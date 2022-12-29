import os

from .base import BASE_DIR

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DATABASE_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DATABASE_USER", "user"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "password"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}
