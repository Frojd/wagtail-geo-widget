from .base import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "wagtailgeowidget": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sites",
    "wagtail.core",
    "wagtail.admin",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.images",
    "taggit",
    "wagtailgeowidget",
    "tests",
]
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = "tests.urls"
SECRET_KEY = "secret key"
