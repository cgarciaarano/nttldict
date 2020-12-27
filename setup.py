#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import find_packages, setup

# Get tag from env that matches lousy semver
VERSION = os.getenv("VERSION", "local")
m = re.search(r"([0-9]+\.){2}[0-9]+", VERSION)
if m:
    VERSION = m[0]

# Package meta-data.
NAME = "nttldict"
DESCRIPTION = "Naive TTL dictionary, with optional on-disk persistence"
INSTALL_REQUIRES = []

TESTS_REQUIRE = ["pytest"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author="Carlos Garcia",
    author_email="cgarciaarano@yahoo.es",
    packages=find_packages(exclude=("tests",)),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    python_requires=">=3.6",
)
