# ******************************************************************************
#
# adapter.py:  django-allauth adapter for 2fa
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
"""Django-allauth adapter for 2fa."""

from urllib.parse import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth_2f2a.utils import user_has_valid_totp_device


class OTPAdapter(DefaultAccountAdapter):
    """Django-allauth OTP adapter."""

    def has_2fa_enabled(self, user):
        """Determine if the user has 2fa configured.

        Returns
        -------
        boolean
            ``True`` if the user has 2fa configured, ``False``
            otherwise.
        """
        return user_has_valid_totp_device(user)

    def login(self, request, user):
        """Require 2fa for login if configured.

        Require 2fa for login if it has been configured by the user.

        Returns
        -------
        allauth.account.adapter.DefaultAccountAdapter
            The original django-allauth account adapter if 2fa is not
            enabled.

        Raises
        ------
        allauth.exceptions.ImmediateHttpResponse
            Redirects to 2fa URL if enabled.
        """
        if self.has_2fa_enabled(user):
            # Cast to string for the case when this is not a JSON
            # serializable object.
            request.session["allauth_2f2a_user_id"] = str(user.id)

            redirect_url = reverse("two-factor-authenticate")
            # Add "next" parameter to the URL.
            view = request.resolver_match.func.view_class()
            view.request = request
            success_url = view.get_success_url()
            query_params = request.GET.copy()
            if success_url:
                query_params[view.redirect_field_name] = success_url
            if query_params:
                redirect_url += "?" + urlencode(query_params)

            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(redirect_url),
            )

        # Otherwise defer to the original allauth adapter.
        return super(OTPAdapter, self).login(request, user)
