#!/usr/bin/env python3

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    LONG_DESCRIPTION = readme.read()

with open("requirements.txt") as handle:
    REQUIRES = handle.read().splitlines()
with open("requirements-test.txt") as handle:
    REQUIRES_TEST = handle.read().splitlines()[1:]

setup(
    name='nijel-thepay',
    python_requires=">=3.5",
    version='0.5',
    author="Michal Čihař",
    author_email="michal@cihar.com",
    description='ThePay API library',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    license='LGPL',
    keywords=["payment", "thepay"],
    url='https://github.com/nijel/thepay',
    packages=find_packages(),
    install_requires=REQUIRES,
    setup_requires=["pytest-runner"],
    tests_require=REQUIRES_TEST,
)
