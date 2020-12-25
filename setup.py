#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "nttldict"
DESCRIPTION = "Naive TTL dictionary, with optional on-disk persistence"
VERSION = os.getenv("VERSION", f'{os.getenv("GIT_COMMIT","local")}')
INSTALL_REQUIRES = []

TESTS_REQUIRE = ["pytest"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author="Carlos Garcia",
    author_email="cgarciaarano@yahoo.es"
    packages=find_packages(exclude=("tests",)),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    python_requires='>=3.6',
)
