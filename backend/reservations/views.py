from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework import serializers

from django.utils.text import format_lazy
from .models import Reservation
from notification.models import Notification
# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/property')
from property.models import Property
from .serializer import ReservationSerializer
from datetime import datetime


# Create your views here.
class CreateReservationView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        # Save user as it's not deserialized
        user = self.request.user
        property_id = self.kwargs['pk']
        property_instance = get_object_or_404(Property, id=property_id)
        host = property_instance.owner

        # check for availability
        availability = property_instance.is_available(validated_data.get("start_date"), validated_data.get("end_date"))
        if not availability:  # Raise validation error if this property is not available
            raise serializers.ValidationError("The reservation request is improper.")

        # current_time = datetime.now()
        notification_content = format_lazy('{} has reserved your property {}', user.get_full_name(),
                                           property_instance.name)
        Notification.create_notification(host, notification_content)
        # Notification.objects.create(target=host, time=current_time, content=notification_content, checked=False)
        serializer.save(user=user, property=property_instance)


class UserUpdateReservationView(UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        instance = super().get_object()
        curr_user = self.request.user
        reservation_user = instance.user
        property_instance = instance.property
        property_owner = property_instance.owner

        # Identity verification
        if curr_user != reservation_user and curr_user != property_owner:
            raise NotAuthenticated("401 Not Authenticated.")

        return instance

        # reservation_instance = super().get_object()
        # curr_user = self.request.user
        # reservation_user = reservation_instance.user
        # if curr_user != reservation_user:
        #     raise NotAuthenticated("401 Not Authenticated.")
        # if reservation_instance.status != "cancelled" and self.request.data.get('status') == "cancelled":
        #     host = reservation_instance.property.owner
        #     current_time = datetime.now()
        #     notification_content = format_lazy('{} has cancelled the reservation with property {}', curr_user.get_full_name(), reservation_instance.property.name)
        #     Notification.objects.create(target=host, time=current_time, content=notification_content, checked=False)
        # return reservation_instance

    def perform_update(self, serializer):
        serializer.save()


# class HostUpdateReservationView(UpdateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         reservation_instance = super().get_object()
#         curr_user = self.request.user
#         host = reservation_instance.property.owner
#         if curr_user != host:
#             raise NotAuthenticated("401 Not Authenticated.")
#         if reservation_instance.status != "approved" and self.request.data.get('status') == "approved":
#             user = reservation_instance.user
#             current_time = datetime.now()
#             notification_content = format_lazy('Your reservation at {} has been approved.', reservation_instance.property.name)
#             Notification.objects.create(target=user, time=current_time, content=notification_content)
#         elif reservation_instance.status != "cancelled" and self.request.data.get('status') == "cancelled":
#             user = reservation_instance.user
#             current_time = datetime.now()
#             notification_content = format_lazy('Your reservation at {} has been cancelled.', reservation_instance.property.name, checked=False)
#             Notification.objects.create(target=user, time=current_time, content=notification_content)
#         return reservation_instance
#
#     def perform_update(self, serializer):
#         serializer.save()


# class DeleteReservationView(DestroyAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         reservation_instance = super().get_object()
#         curr_user = self.request.user
#         reservation_user = reservation_instance.user
#         if curr_user != reservation_user:
#             raise NotAuthenticated("401 Not Authenticated.")
#         host = reservation_instance.property.owner
#         current_time = datetime.now().time()
#         notification_content = format_lazy('{} has canceled the reservation with property {}', curr_user.get_full_name(), reservation_instance.property.name)
#         Notification.objects.create(target=host, time=current_time, content=notification_content)
#         return reservation_instance


class ReservationView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        reservation_instance = super().get_object()
        curr_user = self.request.user
        reservation_user = reservation_instance.user
        property_owner = reservation_instance.property.owner

        if curr_user != reservation_user and curr_user != property_owner:
            raise NotAuthenticated("401 Not Authenticated.")
        return reservation_instance


class HostAllReservationsView(ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        curr_user = self.request.user
        state = self.request.query_params.get('state', None)

        if state:
            return Reservation.objects.filter(property__owner=curr_user, status=state)
        else:
            return curr_user.userReservation_set.all()


class ClientAllReservationsView(ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        curr_user = self.request.user
        state = self.request.query_params.get('state', None)

        if state:
            return Reservation.objects.filter(user=curr_user, status=state)
        else:
            return curr_user.userReservation_set.all()
