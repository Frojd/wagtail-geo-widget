#!/usr/bin/env python

import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


def runtests():
    argv = sys.argv[:1] + ["test"] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.examplesite.settings.test")
    runtests()
