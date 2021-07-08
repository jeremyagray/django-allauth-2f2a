# ******************************************************************************
#
# forms.py:  customized test forms
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
#
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
"""Customized test forms."""

from allauth_2f2a.forms import TOTPAuthenticateForm


class CustomTOTPAuthenticateForm(TOTPAuthenticateForm):
    """Custom TOTP authentication."""

    def __init__(self, *args, **kwargs):
        """Initialize example form for testing."""
        super().__init__(*args, **kwargs)
