from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"friends", views.FriendViewSet, basename="friend")

urlpatterns = []
