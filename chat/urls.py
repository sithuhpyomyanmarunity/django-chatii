from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"conversations", views.ConversationViewSet, basename="conversation")
router.register(r"messages", views.MessageViewSet, basename="message")

urlpatterns = []
