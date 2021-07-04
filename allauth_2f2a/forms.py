# ******************************************************************************
#
# forms.py:  allauth_2f2a forms
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
"""allauth_2f2a forms."""

from django import forms
from django.utils.translation import gettext_lazy as _
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPAuthenticateForm(OTPAuthenticationFormMixin, forms.Form):
    """TOTP authentication form."""

    otp_token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, **kwargs):
        """Initialize the TOTP authentication form."""
        super(TOTPAuthenticateForm, self).__init__(**kwargs)
        self.fields["otp_token"].widget.attrs.update(
            {
                "autofocus": "autofocus",
                "autocomplete": "off",
                "inputmode": "numeric",
            }
        )
        self.user = user

    def clean(self):
        """Clean TOTP authentication form data."""
        self.clean_otp(self.user)
        return self.cleaned_data


class TOTPDeviceForm(forms.Form):
    """TOTP device form."""

    token = forms.CharField(
        label=_("Token"),
    )

    def __init__(self, user, metadata=None, **kwargs):
        """Initialize the TOTP device form."""
        super(TOTPDeviceForm, self).__init__(**kwargs)
        self.fields["token"].widget.attrs.update(
            {
                "autofocus": "autofocus",
                "autocomplete": "off",
            }
        )
        self.user = user
        self.metadata = metadata or {}

    def clean_token(self):
        """Clean the TOTP device token."""
        token = self.cleaned_data.get("token")

        # Find the unconfirmed device and attempt to verify the token.
        self.device = self.user.totpdevice_set.filter(confirmed=False).first()
        if not self.device.verify_token(token):
            raise forms.ValidationError(_("The entered token is not valid"))

        return token

    def save(self):
        """Save the confirmed TOTP device."""
        # The device was found to be valid, delete other confirmed
        # devices and confirm the new device.
        self.user.totpdevice_set.filter(confirmed=True).delete()
        self.device.confirmed = True
        self.device.save()

        return self.device


class TOTPDeviceRemoveForm(forms.Form):
    """TOTP device removal form."""

    def __init__(self, user, **kwargs):
        """Initialize the TOTP device removal form."""
        super(TOTPDeviceRemoveForm, self).__init__(**kwargs)
        self.user = user

    def save(self):
        """Delete the removed TOTP device.

        Delete the removed TOTP device and remove all of its backup
        tokens.
        """
        # Delete any backup tokens.
        static_device = self.user.staticdevice_set.get(name="backup")
        static_device.token_set.all().delete()
        static_device.delete()

        # Delete TOTP device.
        device = TOTPDevice.objects.get(user=self.user)
        device.delete()
