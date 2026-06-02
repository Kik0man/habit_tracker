from django.db import models
from django.conf import settings

class TelegramProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='telegram_profile'
    )
    chat_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram chat ID")
    verified = models.BooleanField(default=False, verbose_name="Верифицирован")

    def __str__(self):
        return f"{self.user.username} - {self.chat_id}"