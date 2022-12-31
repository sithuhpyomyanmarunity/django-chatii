from django.db.models import Prefetch
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friend import serializers

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

__all__ = [
    "ConversationViewSet",
    "MessageViewSet",
]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    def messages(self, request, pk=None):

        messages = (
            Message.objects.filter(conversation=pk)
            .prefetch_related("detail", "reply")
            .order_by("-created_at")
        )
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
        .all()
    )
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     super().perform_create(serializer)

    #     print(serializer.instance)
