from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=255, null=True, blank=True, default=None)

    # class Meta:
    #      app_label = 'TgUser'