import datetime

from django.shortcuts import render
from rest_framework import pagination
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from django.db.models import Q, Max

from accounts.serializers import UserSerializer
from .serializer import NotificationSerializer, MessageSerializer

from accounts.models import User
from .models import Message, Notification


# Create your views here.
class AllNotificationView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(target=user)


# class SendNotification(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = NotificationSerializer
#
#     def perform_create(self, serializer):
#         user_id = self.kwargs['userid']
#         target_user = User.objects.get(id=user_id)
#         serializer.save(target=target_user, time=datetime.datetime.now(), checked=False)


class SingleNotificationView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_object(self):
        user = self.request.user
        notification_id = self.kwargs['pk']
        notification = Notification.objects.get(id=notification_id)
        if user != notification.target:
            raise NotAuthenticated("401 Not Authenticated.")
        notification.checked = True
        notification.save()
        return notification


class CreateMessageView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # url contains target user pk
        user_id = self.kwargs['pk']
        target_user = User.objects.get(id=user_id)
        serializer.save(target=target_user, time=datetime.datetime.now(), checked=False, user=self.request.user)


class ViewMessageWith(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        curr_user = self.request.user
        target_user = User.objects.get(id=self.kwargs['target_id'])
        return Message.objects.filter(
            (Q(user=curr_user) & Q(target=target_user)) |
            (Q(user=target_user) & Q(target=curr_user))
        ).order_by('-time')


class RecentMessageUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        curr_user = self.request.user
        queryset = User.objects.filter(
            Q(sent_messages__user=curr_user) |
            Q(received_messages__target=curr_user)
        ).annotate(
            last_message_time=Max('messageSent_set__time', 'messageGot_set__time')
        ).order_by('-last_message_time')

        return queryset

# class ViewSentMessage(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = MessageSerializer
#     pagination_class = pagination.PageNumberPagination
#
#     def get_queryset(self):
#         curr_user = self.request.user
#         target_user = User.objects.get(id=self.kwargs['target_id'])
#         return Message.objects.filter(user=curr_user, target=target_user).order_by('-time')
#
#
# class ViewReceivedMessage(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = MessageSerializer
#
#     def get_queryset(self):
#         curr_user = self.request.user
#         target_user = User.objects.get(id=self.kwargs['target_id'])
#         return Message.objects.filter(target=curr_user, user=target_user)


# class ViewMessageWith(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = MessageSerializer
#
#     def get_queryset(self):
#         curr_user = self.request.user
#         target_user = User.objects.get(id=self.kwargs['target_id'])
#         messages = Message.objects.filter(Q(target=curr_user, user=target_user) | Q(user=curr_user, target=target_user))
#
#         for message in messages:
#             if message.user == self.request.user:
#                 message.checked = True
#                 message.save()
#
#         return messages





