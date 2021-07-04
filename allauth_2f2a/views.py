# ******************************************************************************
#
# views.py:  allauth_2f2a views
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
"""allauth_2f2a views."""

from base64 import b64encode

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.utils import get_login_redirect_url
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.views.generic import FormView
from django.views.generic import TemplateView
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth_2f2a import app_settings
from allauth_2f2a.forms import TOTPAuthenticateForm
from allauth_2f2a.forms import TOTPDeviceForm
from allauth_2f2a.forms import TOTPDeviceRemoveForm
from allauth_2f2a.mixins import ValidTOTPDeviceRequiredMixin
from allauth_2f2a.utils import generate_totp_config_svg_for_device
from allauth_2f2a.utils import user_has_valid_totp_device


class TwoFactorAuthenticate(FormView):
    """2fa authentication view."""

    template_name = "allauth_2f2a/authenticate." + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPAuthenticateForm

    def dispatch(self, request, *args, **kwargs):
        """Dispatch to correct 2fa authentication view."""
        # Redirect to login if not ready for 2fa.
        if "allauth_2f2a_user_id" not in request.session:
            # Don't use the redirect_to_login here since we don't actually want
            # to include the next parameter.
            return redirect("account_login")

        # Dispatch 2fa authentication.
        return super(TwoFactorAuthenticate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Grab user and insert into ``kwargs``."""
        kwargs = super(TwoFactorAuthenticate, self).get_form_kwargs()
        user_id = self.request.session["allauth_2f2a_user_id"]
        kwargs["user"] = get_user_model().objects.get(id=user_id)
        return kwargs

    def form_valid(self, form):
        """Complete the django-allauth login process.

        The allauth 2fa login flow is now done (the user logged in
        successfully with 2FA), continue the logic from
        allauth.account.utils.perform_login since it was interrupted
        earlier.
        """
        adapter = get_adapter(self.request)

        # Skip over the (already done) 2fa login flow and continue the
        # original allauth login flow.
        super(adapter.__class__, adapter).login(self.request, form.user)

        # Perform the rest of allauth.account.utils.perform_login,
        # this is copied from commit
        # cedad9f156a8c78bfbe43a0b3a723c1a0b840dbd.

        # TODO Support redirect_url.
        response = HttpResponseRedirect(get_login_redirect_url(self.request))

        # TODO Support signal_kwargs.
        signals.user_logged_in.send(
            sender=form.user.__class__,
            request=self.request,
            response=response,
            user=form.user,
        )

        adapter.add_message(
            self.request,
            messages.SUCCESS,
            "account/messages/logged_in.txt",
            {"user": form.user},
        )

        return response


class TwoFactorSetup(LoginRequiredMixin, FormView):
    """2fa setup view."""

    template_name = "allauth_2f2a/setup." + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPDeviceForm
    success_url = reverse_lazy("two-factor-backup-tokens")

    def dispatch(self, request, *args, **kwargs):
        """Dispatch to setup or backup view."""
        # If the user has 2fa configured, redirect them to the backup
        # tokens.
        if user_has_valid_totp_device(request.user):
            return HttpResponseRedirect(reverse("two-factor-backup-tokens"))

        # Continue to 2fa setup otherwise.
        return super(TwoFactorSetup, self).dispatch(request, *args, **kwargs)

    def _new_device(self):
        """Generate a new ``django_otp.plugins.otp_totp.models.TOTPDevice``.

        Replace any unconfirmed TOTPDevices with a new one for
        confirmation.

        This needs to be done whenever a GET request to the page is
        received OR if the confirmation of the device fails.
        """
        self.request.user.totpdevice_set.filter(confirmed=False).delete()
        self.device = TOTPDevice.objects.create(user=self.request.user, confirmed=False)

    def get(self, request, *args, **kwargs):
        """Generate a new TOTP device on every request."""
        self._new_device()
        return super(TwoFactorSetup, self).get(request, *args, **kwargs)

    def get_qr_code_data_uri(self):
        """Return the QR SVG as an encoded data: URI."""
        svg_data = generate_totp_config_svg_for_device(self.request, self.device)
        return "data:image/svg+xml;base64,%s" % force_text(b64encode(svg_data))

    def get_context_data(self, **kwargs):
        """Add ``qr_code_url`` to the context."""
        context = super(TwoFactorSetup, self).get_context_data(**kwargs)
        context["qr_code_url"] = self.get_qr_code_data_uri()
        return context

    def get_form_kwargs(self):
        """Add the user to the form ``kwargs``."""
        kwargs = super(TwoFactorSetup, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Save the device and continue form processing."""
        form.save()
        return super(TwoFactorSetup, self).form_valid(form)

    def form_invalid(self, form):
        """Generate a new device for an invalid form."""
        self._new_device()
        return super(TwoFactorSetup, self).form_invalid(form)


class TwoFactorRemove(ValidTOTPDeviceRequiredMixin, FormView):
    """2fa device removal."""

    template_name = "allauth_2f2a/remove." + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPDeviceRemoveForm
    success_url = reverse_lazy("two-factor-setup")

    def form_valid(self, form):
        """Save the removal data and continue form processing."""
        form.save()
        return super(TwoFactorRemove, self).form_valid(form)

    def get_form_kwargs(self):
        """Add the user to the form ``kwargs``."""
        kwargs = super(TwoFactorRemove, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TwoFactorBackupTokens(ValidTOTPDeviceRequiredMixin, TemplateView):
    """2fa backup token generation."""

    template_name = "allauth_2f2a/backup_tokens." + app_settings.TEMPLATE_EXTENSION
    # This can be overridden in a subclass to ``True``, to have that
    # particular view always reveal the tokens.
    reveal_tokens = bool(app_settings.ALWAYS_REVEAL_BACKUP_TOKENS)

    def get_context_data(self, **kwargs):
        """Add token information to the context.

        Adds ``backup_tokens`` and ``reveal_tokens`` to the view
        context.

        Returns
        -------
        dict
            The context dictionary.
        """
        context = super(TwoFactorBackupTokens, self).get_context_data(**kwargs)
        static_device, _ = self.request.user.staticdevice_set.get_or_create(
            name="backup"
        )

        if static_device:
            context["backup_tokens"] = static_device.token_set.all()
            context["reveal_tokens"] = self.reveal_tokens

        return context

    def post(self, request, *args, **kwargs):
        """Handle 2fa backup POST."""
        static_device, _ = request.user.staticdevice_set.get_or_create(name="backup")
        static_device.token_set.all().delete()
        for _ in range(3):
            static_device.token_set.create(token=StaticToken.random_token())
        self.reveal_tokens = True
        return self.get(request, *args, **kwargs)
