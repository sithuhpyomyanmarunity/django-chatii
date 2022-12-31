from django.conf import settings
from django.db.models import Q
from pusher import Pusher

from chat.models import UserStatus


def get_pusher_client() -> Pusher:
    return Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_APP_KEY,
        secret=settings.PUSHER_APP_SECRET,
        host=settings.PUSHER_HOST,
        port=int(settings.PUSHER_PORT) if settings.PUSHER_PORT else None,
        ssl=False if settings.PUSHER_HOST else True,
    )


def event_channel_occupied(event):
    channel_name: str = event["channel"]

    if channel_name.startswith("User."):
        user_id = channel_name.replace("User.", "")
        status = UserStatus.StatusType.ONLINE

        UserStatus.objects.filter(Q(user=user_id) & ~Q(status=status)).update(
            status=status
        )


def event_channel_vacated(event):
    channel_name = event["channel"]

    if channel_name.startswith("User."):
        user_id = channel_name.replace("User.", "")
        status = UserStatus.StatusType.OFFLINE

        UserStatus.objects.filter(Q(user=user_id) & ~Q(status=status)).update(
            status=status
        )
