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
    from pypandoc import convert_file
    long_description = convert_file("README.md", "rst")
except:  # NOQA
    long_description = ""

version = ''
with io.open('wagtailgeowidget/__init__.py', 'r', encoding='utf8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name="wagtailgeowidget",
    version=version,
    description=("Wagtail-Geo-Widget is the complete map solution for your Wagtail site."),  # NOQA
    long_description=long_description,
    author="Fröjd",
    author_email="martin@marteinn.se",
    url="https://github.com/frojd/wagtail-geo-widget",
    packages=find_packages(exclude=('tests*', 'tests', 'example')),
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Framework :: Django',
        'Topic :: Utilities',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
    ],
)
