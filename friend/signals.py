import random

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAvatar


@receiver(post_save, sender=get_user_model())
def create_user_avatar(sender, instance, created, **kwargs):
    if created:
        user_avatar = UserAvatar(user=instance)
        user_avatar.color = random.choice(UserAvatar.Colors.choices)[0]
        user_avatar.save()
