# ******************************************************************************
#
# mixins.py:  allauth_2f2a mixins
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
"""allauth_2f2a mixins."""

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from allauth_2f2a.utils import user_has_valid_totp_device


class ValidTOTPDeviceRequiredMixin(AccessMixin):
    """Require a valid TOTP device."""

    no_valid_totp_device_url = reverse_lazy("two-factor-setup")

    def dispatch(self, request, *args, **kwargs):
        """Dispatch appropriate view based on device settings."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not user_has_valid_totp_device(request.user):
            return self.handle_missing_totp_device()
        return super(ValidTOTPDeviceRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )

    def handle_missing_totp_device(self):
        """Handle missing device.

        Redirect to ``self.no_valid_totp_device_url`` if there is not
        valid TOTP device configured.

        Returns
        -------
        django.http.HttpResponseRedirect
            A redirect to ``self.no_valid_totp_device_url``.
        """
        return HttpResponseRedirect(self.no_valid_totp_device_url)
