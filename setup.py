# ******************************************************************************
#
# setup.py:  django-allauth-2f2a build setup
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
#
# Copyright 2016-2021 Víðir Valberg Guðmundsson and Percipient
# Networks, LLC.
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
# ******************************************************************************
#
"""django-allauth-2f2a build setup."""

import codecs

from setuptools import find_packages
from setuptools import setup


def long_description():
    """Load README.rst for setup's long description."""
    with codecs.open("README.rst", encoding="utf8") as f:
        return f.read()


setup(
    name="django-allauth-2f2a",
    version="0.8.0",
    packages=find_packages(".", include=("allauth_2f2a", "allauth_2f2a.*")),
    include_package_data=True,
    install_requires=[
        "django>=2.2",
        "qrcode>=5.3",
        "django-allauth>=0.44",
        "django-otp>=1.0.0",
    ],
    author="Jeremy A Gray",
    author_email="gray@flyquackswim.com",
    description="Adds two factor authentication to django-allauth.",
    license="Apache 2.0",
    keywords=["otp", "auth", "two factor authentication", "allauth", "django", "2fa"],
    url="https://github.com/jeremyagray/django-allauth-2f2a",
    long_description=long_description(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Topic :: Internet",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.6",
)
