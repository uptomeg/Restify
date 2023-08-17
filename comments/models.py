from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/property')
from property.models import Property

# sys.path.insert(1, '/group_2256/P2/restify/p2/accounts')
from accounts.models import User


class UserComment(models.Model):
    rating = models.IntegerField(null=True, validators=[MaxValueValidator(10), MinValueValidator(0)])
    under = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='userComment_set')
    content = models.CharField(max_length=300, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment_set')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=False)


class PropertyComment(models.Model):
    rating = models.IntegerField(null=True, validators=[MaxValueValidator(10), MinValueValidator(0)])
    under = models.ForeignKey(Property, on_delete=models.SET_NULL, related_name='propertyComment_set', null=True)
    content = models.CharField(max_length=300, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='userPropertyComment_set')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=False)

