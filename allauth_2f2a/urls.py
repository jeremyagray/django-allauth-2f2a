# ******************************************************************************
#
# urls.py:  URL routing for allauth_2f2a module
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
"""URL routing for allauth_2f2a module."""

from django.conf.urls import url

from allauth_2f2a import views

urlpatterns = [
    url(
        r"^two-factor-authenticate/?$",
        views.TwoFactorAuthenticate.as_view(),
        name="two-factor-authenticate",
    ),
    url(
        r"^two_factor/setup/?$", views.TwoFactorSetup.as_view(), name="two-factor-setup"
    ),
    url(
        r"^two_factor/backup_tokens/?$",
        views.TwoFactorBackupTokens.as_view(),
        name="two-factor-backup-tokens",
    ),
    url(
        r"^two_factor/remove/?$",
        views.TwoFactorRemove.as_view(),
        name="two-factor-remove",
    ),
]
