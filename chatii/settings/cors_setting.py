from .base import ENVIRONMENT

if ENVIRONMENT != "local":
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:6001",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:6001",
]
