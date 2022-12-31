from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from .serializers import FriendSerializer

__all__ = ["FriendViewSet"]


class FriendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        get_user_model()
        .objects.filter(is_staff=False, is_superuser=False, is_active=True)
        .order_by("first_name", "last_name")
    )
    serializer_class = FriendSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["username", "first_name", "last_name"]

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)
