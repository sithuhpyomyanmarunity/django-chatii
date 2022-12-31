from .pusher import get_pusher_client


def send_pusher_notification(event: str, users: list, data):
    pusher_client = get_pusher_client()
    channels = [f"User.{user}" for user in users]

    pusher_client.trigger(
        channels=channels,
        event_name="notification",
        data={
            "event": event,
            "payload": data,
        },
    )
