import dj_database_url
from decouple import config

from .base import *


DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = []

# Database

DB_URI = (
    f'{config("db_schema", str)}://{config("db_user")}:{config("db_password")}'
    + f'@{config("db_host")}:{config("db_port")}/{config("db_name")}'
)

DATABASES = {"default": dj_database_url.config(default=DB_URI)}

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
