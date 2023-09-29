from django.db import models
from django.utils import timezone

#from ..accounts.models import User
# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/accounts')
from accounts.models import User


# Create your models here.
class Notification(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False)
    target = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(null=False)
    checked = models.BooleanField(null=False)

    @classmethod
    def create_notification(cls, target_user, content):
        new_notification = cls(
            content=content,
            target=target_user,
            time=timezone.now(),
            checked=False
        )
        new_notification.save()
        return new_notification


class Message(models.Model):
    content = models.CharField(max_length=500, null=False, blank=False)
    time = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messageSent_set', null=True)
    target = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messageGot_set', null=True)
    checked = models.BooleanField(null=False)
