from decouple import config

from .base import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = ["127.0.0.1"]

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Installed apps definition for development environment

# Adding and configuring Drf_spectacular

INSTALLED_APPS.append("drf_spectacular")
REST_FRAMEWORK.update({"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"})
SPECTACULAR_SETTINGS = {
    "TITLE": "Project API",
    "DESCRIPTION": "API Schema for the project",
    "VERSION": "0.5.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
