#!/usr/bin/env python
import inspect
import os
import sys

import dotenv


def if_exists_load_env(name: str) -> None:
    current_frame = inspect.currentframe()
    if not current_frame:
        return

    inspect_file = inspect.getfile(current_frame)
    env_path = os.path.dirname(os.path.abspath(inspect_file))
    env_file = "{env_path}/{name}".format(env_path=env_path, name=name)

    if os.path.exists(env_file):
        dotenv.load_dotenv(env_file, override=True)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.examplesite.settings.dev")

    if_exists_load_env(".env.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
