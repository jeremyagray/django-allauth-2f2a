# ******************************************************************************
#
# settings.py:  settings for test project
#
# SPDX-License-Identifier: Apache-2.0
#
# ******************************************************************************
#
# Copyright 2016 Percipient Networks, LLC.
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
"""Settings for test project."""

import django

SECRET_KEY = "not_empty"
SITE_ID = 1
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"
LOGIN_REDIRECT_URL = "/accounts/password/change/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

INSTALLED_APPS = (
    # Required by allauth.
    "django.contrib.sites",
    # Configure Django auth package.
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # Enable allauth.
    "allauth",
    "allauth.account",
    # Required to render the default template for 'account_login'.
    "allauth.socialaccount",
    # Configure the django-otp package.
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    # Enable two-factor auth.
    "allauth_2f2a",
    # Test app.
    "tests",
)

MIDDLEWARE = (
    # Configure Django auth package.
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Configure the django-otp package.
    "django_otp.middleware.OTPMiddleware",
    # Reset login flow middleware.
    "allauth_2f2a.middleware.AllauthTwoFactorMiddleware",
)

if django.VERSION < (2,):
    MIDDLEWARE += ("django.contrib.auth.middleware.SessionAuthenticationMiddleware",)

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Enable two-factor auth.
ACCOUNT_ADAPTER = "allauth_2f2a.adapter.OTPAdapter"
