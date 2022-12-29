from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserStatus


@receiver(post_save, sender=get_user_model())
def create_user_status(sender, instance, created, **kwargs):
    if created:
        user_status = UserStatus(user=instance)
        user_status.save()
