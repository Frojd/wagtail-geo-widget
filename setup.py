#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import re
from setuptools import setup, find_packages


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open('README.md') as f:
    readme = f.read()

# Convert markdown to rst
try:
    from pypandoc import convert
    long_description = convert("README.md", "rst")
except:
    long_description = ""

version = ''
with io.open('wagtailgeowidget/__init__.py', 'r', encoding='utf8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name="wagtailgeowidget",
    version=version,
    description=("A Google Maps widget for Wagtail that supports both GeoDjango PointField, StreamField and CharField."),  # NOQA
    long_description=long_description,
    author="Fröjd",
    author_email="martin@marteinn.se",
    url="https://github.com/frojd/wagtail-geo-widget",
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Framework :: Django',
        'Topic :: Utilities',
    ],
)
