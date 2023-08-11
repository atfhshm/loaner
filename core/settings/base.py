"""
Django project base settings
"""

from pathlib import Path
from datetime import timedelta
from decouple import config


from ..logging import LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Secret Key
SECRET_KEY = config("SECRET_KEY")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # Project apps
    "users.apps.UsersConfig",
    "funds.apps.FundsConfig",
    "loans.apps.LoansConfig",
]

# Middleware definition

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third-party middleware
    "corsheaders.middleware.CorsMiddleware",
]

# Django-REST framework settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("SECRET_KEY", cast=str),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# CORS settings

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Root URLS file for the project

ROOT_URLCONF = "core.urls"

# Default templates definition

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

# STATICFILE_DIR = BASE_DIR.joinpath("static/")
# STATICFILES_DIRS = (STATICFILE_DIR,)


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.joinpath("staticfiles/")

# Media files (user uploaded media)

MEDIA_URL = "/uploads/"
MEDIA_ROOT = BASE_DIR.joinpath("media/")


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Setting the default user model for custom user models

AUTH_USER_MODEL = "users.User"


# Redis settings

# REDIS_PROTOCOL = config("REDIS_PROTOCOL", "redis")
# REDIS_USERNAME = config("REDIS_USER", "")
# REDIS_PASSWORD = config("REDIS_PASSWORD", "")
# REDIS_HOST = config("REDIS_HOST", "redis")
# REDIS_PORT = config("REDIS_PORT", "6379")
# REDIS_URL = config(
#     "REDIS_URL",
#     default=f"{REDIS_PROTOCOL}://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/",
# )


# Django channels settings

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL],
#         },
#     },
# }

# Celery settings

# CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL

# Email settings

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# DEFAULT_FROM_EMAIL = config("DEFAULT_EMAIL_SMTP_USER", "")
# EMAIL_HOST_USER = config("EMAIL_SMTP_USER", "")
# EMAIL_HOST_PASSWORD = config("EMAIL_SMTP_PASSWORD", "")
# EMAIL_HOST = config("EMAIL_SMTP_HOST", "localhost")
# EMAIL_PORT = config("EMAIL_SMTP_PORT")


# Caching settings
