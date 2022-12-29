from django.contrib.auth import get_user_model
from rest_framework import viewsets

# Create your views here.
from .serializers import FriendSerializer

__all__ = ["FriendViewSet"]


class FriendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.filter(
        is_staff=False, is_superuser=False, is_active=True
    )
    serializer_class = FriendSerializer
