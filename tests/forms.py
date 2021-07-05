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

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

from allauth_2f2a.forms import TOTPAuthenticateForm


class CrispyTOTPAuthenticateForm(TOTPAuthenticateForm):
    """Crispy TOTP authentication."""

    def __init__(self, *args, **kwargs):
        """Crispy form example for testing."""
        super().__init__(*args, **kwargs)

        # Add the crispy forms helper.
        # self.helper = FormHelper(self)
        # self.helper.form_method = "post"
        # self.helper.layout.append(
        #     Submit("submit", "Authenticate", css_class="btn-primary"),
        # )
