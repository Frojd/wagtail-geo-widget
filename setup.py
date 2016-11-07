#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import pip
from setuptools import setup, find_packages
from pip.req import parse_requirements


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open('README.md') as f:
    readme = f.read()

# Handle requirements
requires = parse_requirements("requirements/install.txt",
                              session=pip.download.PipSession())
install_requires = [str(ir.req) for ir in requires]

# Convert markdown to rst
try:
    from pypandoc import convert
    long_description = convert("README.md", "rst")
except:
    long_description = ""

version = ''
with open('wagtailgeowidget/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name="wagtailgeowidget",
    version=version,
    description=("Google Maps widget for the GeoDjango PointField field in Wagtail"),  # NOQA
    long_description=long_description,
    author="Fröjd",
    author_email="martin@marteinn.se",
    url="https://github.com/frojd/wagtail-geo-widget",
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    install_requires=install_requires,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7",
        'Framework :: Django',
        'Topic :: Utilities',
    ],
)
