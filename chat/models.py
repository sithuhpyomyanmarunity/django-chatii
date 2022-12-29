import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import Q
from django.utils.functional import lazy

# Create your models here.


class Conversation(models.Model):
    class ConversationType(models.TextChoices):
        PRIVATE = "private", "Private"
        GROUP = "group", "Group"

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    conversation_type = models.CharField(
        "", max_length=50, choices=ConversationType.choices
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Participant"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Participant(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participant"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="participant"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        unique_together = ("user", "conversation")


def get_message_content():
    return [c.__name__.lower() for c in MessageContent.__subclasses__()]


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    conversation = models.ForeignKey(
        Conversation(), on_delete=models.CASCADE, null=True, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="msesages",
    )
    reply = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="message",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": lazy(get_message_content, list)()},
    )
    object_id = models.UUIDField()
    detail = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class MessageContent(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    message = GenericRelation(Message)

    class Meta:
        abstract = True


class TextMessage(MessageContent):
    content = models.TextField(max_length=5000)


class UserStatus(models.Model):
    class StatusType(models.IntegerChoices):
        OFFLINE = 0, "Offline"
        ONLINE = 1, "Online"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    status = models.SmallIntegerField(
        default=StatusType.OFFLINE, choices=StatusType.choices, db_index=True
    )
