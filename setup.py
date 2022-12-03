#!/usr/bin/env python

import io
import re
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = ""
with io.open("wagtailgeowidget/__init__.py", "r", encoding="utf8") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

test_extras = [
    "pytest",
    "pytest-django",
    "factory-boy",
]

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
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    extras_require={"test": test_extras},
    install_requires=[
        "Wagtail>=2.15",
    ],
    project_urls={
        "Source": "https://github.com/Frojd/wagtail-geo-widget/",
        "Changelog": "https://github.com/Frojd/wagtail-geo-widget/blob/main/CHANGELOG.md",
    },
)
