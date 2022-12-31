from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from chat.pusher import event_channel_occupied, event_channel_vacated, get_pusher_client

from .filters import MessageFilter
from .models import Conversation, Message, Participant, UserStatus
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    PusherPayloadSerializer,
)
from .utils import send_pusher_notification


@login_required
def chat(request: HttpRequest) -> HttpResponse:
    return render(request, "chat/chat.html", {"user": request.user})


@csrf_exempt
@api_view(["POST"])
def pusher_webhook(request: Request):
    # key = request.stream.headers.get("X-PUSHER-KEY")
    # signature = request.stream.headers.get("X-PUSHER-SIGNATURE")
    # get_pusher_client().validate_webhook()
    serializer = PusherPayloadSerializer(request.data)

    for event in serializer.data["events"]:
        if event["name"] == "channel_occupied":
            event_channel_occupied(event)
        elif event["name"] == "channel_vacated":
            event_channel_vacated(event)
    return HttpResponse("ok")


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.order_by("-updated_at").all()
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    def messages(self, request: Request, pk=None):

        messages = MessageFilter(
            request.query_params,
            queryset=Message.objects.filter(conversation=pk)
            .prefetch_related("detail", "reply", "sender__avatar")
            .select_related("conversation")
            .order_by("-created_at"),
        ).qs[:15]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        return (
            super()
            .filter_queryset(queryset)
            .filter(participant__user=self.request.user)
        )

    def get_queryset(self):

        if self.action != "list":
            return super().get_queryset()

        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=Message.objects.prefetch_related("detail")
                    .order_by("conversation", "-created_at")
                    .distinct("conversation"),
                )
            )
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = (
        Message.objects.order_by("-created_at")
        .prefetch_related("detail", "reply")
        .select_related("conversation")
        .all()
    )
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        message.conversation.save(update_fields=["updated_at"])
        self.send_notification("new-message", message=message)

    @transaction.atomic
    def perform_update(self, serializer):
        message = serializer.save(sender=self.request.user)
        message.conversation.save(update_fields=["updated_at"])
        self.send_notification("update-message", message=message)

    def send_notification(self, event_name: str, message: Message):
        serializer = self.get_serializer_class()(message)

        participants = UserStatus.objects.filter(
            user__in=Participant.objects.filter(conversation=message.conversation)
            .exclude(user=self.request.user)
            .values_list("user", flat=True),
            status=UserStatus.StatusType.ONLINE,
        ).values_list("user", flat=True)

        notification_payload = serializer.data

        if "conversation_id" in notification_payload:
            notification_payload["conversation_id"] = str(
                notification_payload["conversation_id"]
            )

        if len(participants) > 0:
            send_pusher_notification(event_name, participants, notification_payload)
