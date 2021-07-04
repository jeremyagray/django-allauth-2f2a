# ******************************************************************************
#
# urls.py:  test project URL routing
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
"""Test project URL routing."""

from django.conf.urls import include
from django.conf.urls import url
from django.http import HttpResponse


def blank_view(request):
    """Return the hellow world view."""
    return HttpResponse("<h1>HELLO WORLD!</h1>")


urlpatterns = [
    # Include the allauth and 2FA urls from their respective packages.
    url(r"^accounts/", include("allauth_2f2a.urls")),
    url(r"^accounts/", include("allauth.urls")),
    # A view without a name.
    url(r"^unnamed-view$", blank_view),
]
