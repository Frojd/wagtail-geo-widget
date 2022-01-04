#!/usr/bin/env python

import io
import os
import re
import sys
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = ""
with io.open("wagtailgeowidget/__init__.py", "r", encoding="utf8") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="wagtailgeowidget",
    version=version,
    description=(
        "Wagtail-Geo-Widget is the complete map solution for your Wagtail site."
    ),  # NOQA
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fröjd",
    author_email="martin@marteinn.se",
    url="https://github.com/frojd/wagtail-geo-widget",
    packages=find_packages(exclude=("tests*", "tests", "example")),
    include_package_data=True,
    install_requires=[
        "Django>=2.2",
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Topic :: Utilities",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
    ],
)
