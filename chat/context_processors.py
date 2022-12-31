from django.conf import settings


def pusher(request):
    return {
        "PUSHER_APP_KEY": settings.PUSHER_APP_KEY,
        "PUSHER_HOST": settings.PUSHER_HOST,
        "PUSHER_PORT": settings.PUSHER_PORT,
    }
