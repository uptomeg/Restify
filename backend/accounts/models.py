from django.db import models
from django.contrib.auth.models import AbstractUser
# from PIL import Image


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
