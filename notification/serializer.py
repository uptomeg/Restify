from rest_framework.serializers import ModelSerializer

# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/notification')
from notification.models import Notification, Message


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('time', 'checked', 'target')


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('user', 'time', 'checked')

