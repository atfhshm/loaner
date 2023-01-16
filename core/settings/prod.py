from decouple import config

from .base import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = [config("ALLOWED_HOST")]

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME", cast=str),
#         "USER": config("DB_USER", cast=str),
#         "PASSWORD": config("DB_PASSWORD", cast=str),
#         "HOST": config("DB_HOST", cast=str),
#         "PORT": config("BD_PORT", cast=str),
#     }
# }
