from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import sys

from notification.models import Notification
from reservations.models import Reservation


# sys.path.insert(1, '/group_2256/P2/restify/p2/reservations')
# from reservations.models import Reservation


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user',)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        new_status = validated_data.get('status', instance.status)
        notification_content = ''

        if user == instance.user:
            if instance.status in ['pending', 'approved'] and new_status in ['cancelled', 'completed']:
                instance.status = new_status
                notification_content = f"Reservation status updated to {new_status} by the user."
            else:
                raise serializers.ValidationError("You are not authorized to update the reservation status.")
        elif user == instance.property.owner:
            if instance.status == 'pending' and new_status in ['approved', 'terminated']:
                instance.status = new_status
                notification_content = f"Reservation status updated to {new_status} by the property owner."
            elif instance.status == 'approved' and new_status == 'terminated':
                instance.status = new_status
                notification_content = f"Reservation status updated to {new_status} by the property owner."
            else:
                raise serializers.ValidationError("You are not authorized to update the reservation status.")
        else:
            raise serializers.ValidationError("You are not authorized to update the reservation status.")

        instance.save()

        # Create a new notification instance
        target_user = instance.user if user == instance.property.owner else instance.property.owner
        Notification.create_notification(target_user, notification_content)

        return instance
