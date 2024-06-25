from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    phone_number = models.CharField(max_length=50)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self) -> str:
        return self.user.username
