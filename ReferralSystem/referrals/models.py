from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    auth_code = models.CharField(max_length=4, blank=True, null=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)
    referral = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username