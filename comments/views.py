import datetime

from django.shortcuts import render, get_object_or_404
from rest_framework import pagination
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from django.db import models
# import sys

from .serializer import UserCommentSerializer, PropertyCommentSerializer
from .models import UserComment, PropertyComment
# sys.path.insert(1, '/group_2256/P2/restify/p2/accounts')
from accounts.models import User
# sys.path.insert(1, '/group_2256/P2/restify/p2/property')
from property.models import Property

# Create your views here.


class UserCommentView(ListAPIView):
    serializer_class = UserCommentSerializer
    pagination_class = pagination.PageNumberPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        target_id = self.kwargs['pk']
        target_user = get_object_or_404(User, id=target_id)
        current_user = self.request.user
        return UserComment.objects.filter(owner__id=current_user.id, under__id=target_user.id)


class LeaveComment(CreateAPIView):
    serializer_class = UserCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        under_id = self.kwargs['pk']
        target_user = User.objects.get(id=under_id)
        serializer.save(owner=self.request.user, under=target_user, parent=None, date=datetime.datetime.now())


class SingleComment(RetrieveAPIView):
    serializer_class = UserCommentSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserComment, id=self.kwargs['pk'])


class DeleteUserComment(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentSerializer

    def get_object(self):
        curr_user = self.request.user
        obj_id = self.kwargs['pk']
        instance = UserComment.objects.get(id=obj_id)
        if curr_user != instance.owner:
            raise NotAuthenticated("401 Not Authenticated.")
        return instance


class ReplyUserComment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentSerializer

    def perform_create(self, serializer):
        parent_id = self.kwargs['pk']
        parent = get_object_or_404(UserComment, id=parent_id)
        serializer.save(owner=self.request.user, under=parent.under, parent=parent, date=datetime.datetime.now())


class UpdateUserComment(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentSerializer

    def get_object(self):
        user_id = self.request.user.id
        comment_id = self.kwargs['pk']
        comment = UserComment.objects.get(id=comment_id)
        if comment.owner.id != user_id:
            raise NotAuthenticated("401 Not Authenticated.")
        return comment


class CreatePropertyComment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertyCommentSerializer

    def perform_create(self, serializer):
        property_id = self.kwargs['pk']
        # duplicate = PropertyComment.objects.get(under_id=property_id, owner=self.request.user)
        # if duplicate and duplicate.parent is None:
        #     raise NotAuthenticated("You can leave at most 1 comment")
        target_property = Property.objects.get(id=property_id)
        serializer.save(under=target_property, owner=self.request.user, parent=None, date=datetime.datetime.now())


class PropertyCommentView(ListAPIView):
    serializer_class = PropertyCommentSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        target_id = self.kwargs['pk']
        target = Property.objects.get(id=target_id)
        return target.propertyComment_set.all()


class UpdatePropertyCommentView(UpdateAPIView):
    serializer_class = PropertyCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        curr_user = self.request.user
        comment_id = self.kwargs['pk']
        comment = PropertyComment.objects.get(id=comment_id)
        if comment.owner.id != curr_user.id:
            raise NotAuthenticated("401 Not Authenticated.")
        return comment


class DeletePropertyCommentView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertyCommentSerializer
    queryset = PropertyComment.objects.all()

    def get_object(self):
        instance = super().get_object()
        curr_user = self.request.user
        if instance.owner != curr_user:
            raise NotAuthenticated("401 Not Authenticated.")
        return instance


class ReplyPropertyComment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertyCommentSerializer

    def perform_create(self, serializer):
        parent_id = self.kwargs['pk']
        parent = get_object_or_404(PropertyComment, id=parent_id)
        serializer.save(owner=self.request.user, under=parent.under, parent=parent, date=datetime.datetime.now())


class SinglePropertyCommentView(RetrieveAPIView):
    serializer_class = PropertyCommentSerializer

    def get_object(self):
        return get_object_or_404(PropertyComment, id=self.kwargs['pk'])





