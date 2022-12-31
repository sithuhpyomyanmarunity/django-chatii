from django.conf import settings
from django.db import models


# Create your models here.
class UserAvatar(models.Model):
    class Colors(models.TextChoices):
        RED = "text-white bg-rose-500", "Red"
        GREEN = "text-white bg-emerald-400", "Green"
        BLUE = "text-blue-600 bg-sky-100", "Blue"
        YELLOW = "text-black bg-amber-300", "Yellow"
        EMERALD = "text-emerald-600 bg-emerald-200", "Emerald"
        VIOLET = "text-violet-600 bg-violet-200", "VIOLET"
        GRAY = "text-slate-800 bg-slate-200", "Gray"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="avatar",
    )
    color = models.CharField(max_length=255)
    image = models.FileField(null=True)
