from django.contrib import auth
from django.db import models
from django.utils import timezone


class CustomUser(auth.models.AbstractUser):

    def __str__(self):
        return "@{}".format(self.email)

# class Profile(models.Model):
#     user_profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     department = models.CharField(max_length=100, default="No department specified")
#
#     def __str__(self):
#         return self.user_profile.username
