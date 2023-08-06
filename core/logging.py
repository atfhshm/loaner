LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "[%(asctime)s] %(log_color)s%(levelname)s %(reset)s %(blue)s%(message)s",
        },
        "standard": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        }
    },
    "loggers": {
        logger_name: {"level": "DEBUG", "propagate": True}
        for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
            "core",
        )
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}
