from .base import *

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sites",
    "wagtail",
    "wagtail.admin",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.images",
    "taggit",
    "wagtailgeowidget",
    "tests.examplesite",
    "tests.home",
    "tests.search",
    "tests.geopage",
    "tests.geopage_nospatial",
    "tests",
]

MIDDLEWARE_CLASSES = []

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

SECRET_KEY = "RANDOM"
