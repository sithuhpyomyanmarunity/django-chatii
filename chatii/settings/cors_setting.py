from .base import ENVIRONMENT

if ENVIRONMENT != "local":
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = True
