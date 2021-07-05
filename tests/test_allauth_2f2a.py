# ******************************************************************************
#
# test_allauth_2f2a.py:  allauth_2f2a tests
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
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
"""allauth_2f2a tests."""

from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse

from allauth.account.signals import user_logged_in
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django_otp.oath import TOTP
from pyfakefs.fake_filesystem_unittest import patchfs

from allauth_2f2a import app_settings
from allauth_2f2a.middleware import BaseRequire2FAMiddleware


def normalize_url(url):
    """Sort the URL query string parameters."""
    url = str(url)  # Coerce reverse_lazy() URLs.
    scheme, netloc, path, params, query, fragment = urlparse(url)
    query_parts = sorted(parse_qsl(query))

    return urlunparse(
        (
            scheme,
            netloc,
            path,
            params,
            urlencode(query_parts),
            fragment,
        )
    )


class Test2Factor(TestCase):
    """2fa tests."""

    def setUp(self):
        """Set up Test2Factor()."""
        self.user_logged_in_count = 0
        user_logged_in.connect(self._login_callback)

    def tearDown(self):
        """Reset after each test."""
        # Set TWOFA_FORMS to default.
        setattr(
            app_settings,
            "TWOFA_FORMS",
            {
                "authenticate": "allauth_2f2a.forms.TOTPAuthenticateForm",
                "device": "allauth_2f2a.forms.TOTPDeviceForm",
                "remove": "allauth_2f2a.forms.TOTPDeviceRemoveForm",
            },
        )

    def _login_callback(self, sender, **kwargs):
        """Increment the login count."""
        self.user_logged_in_count += 1

    def test_standard_login(self):
        """Should login if 2fa is not configured."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            settings.LOGIN_REDIRECT_URL,
            fetch_redirect_response=False,
        )

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_2fa_login(self):
        """Should login when 2fa is configured."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            reverse("two-factor-authenticate"),
            fetch_redirect_response=False,
        )

        # Now ensure that logging in actually works.
        totp = TOTP(
            totp_model.bin_key,
            totp_model.step,
            totp_model.t0,
            totp_model.digits,
        )
        resp = self.client.post(
            reverse("two-factor-authenticate"),
            {"otp_token": totp.token()},
        )
        self.assertRedirects(
            resp,
            settings.LOGIN_REDIRECT_URL,
            fetch_redirect_response=False,
        )

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_2fa_login_custom_form(self):
        """Should login when 2fa is configured."""
        setattr(
            app_settings,
            "TWOFA_FORMS",
            {
                "authenticate": "tests.forms.CrispyTOTPAuthenticateForm",
                "device": "allauth_2f2a.forms.TOTPDeviceForm",
                "remove": "allauth_2f2a.forms.TOTPDeviceRemoveForm",
            },
        )

        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            reverse("two-factor-authenticate"),
            fetch_redirect_response=False,
        )

        # Now ensure that logging in actually works.
        totp = TOTP(
            totp_model.bin_key,
            totp_model.step,
            totp_model.t0,
            totp_model.digits,
        )
        resp = self.client.post(
            reverse("two-factor-authenticate"),
            {"otp_token": totp.token()},
        )
        self.assertRedirects(
            resp,
            settings.LOGIN_REDIRECT_URL,
            fetch_redirect_response=False,
        )

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_invalid_2fa_login(self):
        """Should not login when wrong 2fa code is provided."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            reverse("two-factor-authenticate"),
            fetch_redirect_response=False,
        )

        # Ensure that logging in does not work with invalid token
        resp = self.client.post(
            reverse("two-factor-authenticate"),
            {"otp_token": "invalid"},
        )
        self.assertEqual(resp.status_code, 200)

    def test_2fa_redirect(self):
        """Should redirect if 2fa is not necessry."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()

        # Not logged in.
        resp = self.client.get(reverse("two-factor-authenticate"))
        self.assertRedirects(
            resp,
            reverse("account_login"),
            fetch_redirect_response=False,
        )

        # Logged in.
        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )

        resp = self.client.get(reverse("two-factor-authenticate"))
        self.assertRedirects(
            resp,
            reverse("account_login"),
            fetch_redirect_response=False,
        )

    def test_2fa_reset_flow(self):
        """Should redirect to login on 2fa interruption."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"), {"login": "john", "password": "doe"}
        )
        self.assertRedirects(
            resp, reverse("two-factor-authenticate"), fetch_redirect_response=False
        )

        # The user ID should be in the session.
        self.assertIn("allauth_2f2a_user_id", self.client.session)

        # Navigate to a different page.
        self.client.get(reverse("account_login"))

        # The middleware should reset the login flow.
        self.assertNotIn("allauth_2f2a_user_id", self.client.session)

        # Trying to continue with two-factor without logging in again will
        # redirect to login.
        resp = self.client.get(reverse("two-factor-authenticate"))

        self.assertRedirects(
            resp, reverse("account_login"), fetch_redirect_response=False
        )

    def test_2fa_login_forwarding_get_parameters(self):
        """Should pass route parameters through 2fa views."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        user.totpdevice_set.create()

        # Add a next to unnamed-view.
        resp = self.client.post(
            reverse("account_login") + "?existing=param&next=unnamed-view",
            {"login": "john", "password": "doe"},
            follow=True,
        )

        # Ensure that the unnamed-view is still being forwarded to.
        resp.redirect_chain[-1] = (
            normalize_url(resp.redirect_chain[-1][0]),
            resp.redirect_chain[-1][1],
        )
        self.assertRedirects(
            resp,
            normalize_url(
                reverse("two-factor-authenticate")
                + "?existing=param&next=unnamed-view",
            ),
            fetch_redirect_response=False,
        )

    def test_2fa_login_forwarding_next_via_post(self):
        """Should respect ``next`` parameter on POST."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        user.totpdevice_set.create()

        # Add a next to unnamed-view.
        resp = self.client.post(
            reverse("account_login") + "?existing=param",
            {"login": "john", "password": "doe", "next": "unnamed-view"},
            follow=True,
        )

        # Ensure that the unnamed-view is still being forwarded to,
        # preserving existing query params.
        resp.redirect_chain[-1] = (
            normalize_url(resp.redirect_chain[-1][0]),
            resp.redirect_chain[-1][1],
        )
        self.assertRedirects(
            resp,
            normalize_url(
                reverse("two-factor-authenticate") + "?existing=param&next=unnamed-view"
            ),
            fetch_redirect_response=False,
        )

    def test_anonymous(self):
        """Anonymous users should not access 2fa views."""
        # The authentication page redirects to the login page.
        url = reverse("two-factor-authenticate")
        resp = self.client.get(url)
        self.assertRedirects(
            resp, reverse("account_login"), fetch_redirect_response=False
        )

        # Some pages redirect to the login page and then will redirect back.
        for url in [
            "two-factor-setup",
            "two-factor-backup-tokens",
            "two-factor-remove",
        ]:
            url = reverse(url)
            resp = self.client.get(url)
            self.assertRedirects(
                resp,
                reverse("account_login") + "?next=" + url,
                fetch_redirect_response=False,
            )

    def test_unnamed_view(self):
        """Should reset login if 2fa is interrupted."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"), {"login": "john", "password": "doe"}
        )
        self.assertRedirects(
            resp, reverse("two-factor-authenticate"), fetch_redirect_response=False
        )

        # The user ID should be in the session.
        self.assertIn("allauth_2f2a_user_id", self.client.session)

        # Navigate to a different (unnamed) page.
        resp = self.client.get("/unnamed-view")

        # The middleware should reset the login flow.
        self.assertNotIn("allauth_2f2a_user_id", self.client.session)

        # Trying to continue with two-factor without logging in again
        # will redirect to login.
        resp = self.client.get(reverse("two-factor-authenticate"))

        self.assertRedirects(
            resp, reverse("account_login"), fetch_redirect_response=False
        )

    def test_backwards_compatible_url(self):
        """Should still work."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            reverse("two-factor-authenticate"),
            fetch_redirect_response=False,
        )

        # Now ensure that logging in actually works.
        totp = TOTP(
            totp_model.bin_key,
            totp_model.step,
            totp_model.t0,
            totp_model.digits,
        )

        # The old URL doesn't have a trailing slash.
        url = reverse("two-factor-authenticate").rstrip("/")

        resp = self.client.post(url, {"otp_token": totp.token()})
        self.assertRedirects(
            resp,
            settings.LOGIN_REDIRECT_URL,
            fetch_redirect_response=False,
        )

        # Ensure the signal is received as expected.
        self.assertEqual(self.user_logged_in_count, 1)

    def test_not_configured_redirect(self):
        """Should redirect if 2fa is not configured."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()

        # Login.
        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )

        # The 2FA pages should redirect.
        for url_name in ["two-factor-backup-tokens", "two-factor-remove"]:
            resp = self.client.get(reverse(url_name))
            self.assertRedirects(
                resp,
                reverse("two-factor-setup"),
                fetch_redirect_response=False,
            )


class Require2FA(BaseRequire2FAMiddleware):
    """Require 2fa if configured."""

    def require_2fa(self, request):
        """Determine if 2fa is required if configured."""
        return True


@override_settings(
    # Don't redirect to an "allowed" URL.
    LOGIN_REDIRECT_URL="/unnamed-view",
    # Add the middleware that requires 2FA.
    MIDDLEWARE=settings.MIDDLEWARE + ("tests.test_allauth_2f2a.Require2FA",),
)
class TestRequire2FAMiddleware(TestCase):
    """2fa middleware tests."""

    def test_no_2fa(self):
        """Should redirect to setup if 2fa is not configured."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
            follow=True,
        )
        # The user is redirected to the 2FA setup page.
        self.assertRedirects(
            resp,
            reverse("two-factor-setup"),
            fetch_redirect_response=False,
        )

    def test_2fa(self):
        """Should login when 2fa is configured."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        totp_model = user.totpdevice_set.create()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
        )
        self.assertRedirects(
            resp,
            reverse("two-factor-authenticate"),
            fetch_redirect_response=False,
        )

        # Now ensure that logging in actually works.
        totp = TOTP(
            totp_model.bin_key,
            totp_model.step,
            totp_model.t0,
            totp_model.digits,
        )
        resp = self.client.post(
            reverse("two-factor-authenticate"),
            {"otp_token": totp.token()},
        )
        # The user ends up on the normal redirect login page.
        self.assertRedirects(
            resp,
            settings.LOGIN_REDIRECT_URL,
            fetch_redirect_response=False,
        )

    @override_settings(
        INSTALLED_APPS=settings.INSTALLED_APPS + ("django.contrib.messages",),
        # This doesn't seem to stack nicely with the class-based one,
        # so add the middleware here.
        MIDDLEWARE=settings.MIDDLEWARE
        + (
            "tests.test_allauth_2f2a.Require2FA",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
    )
    def test_no_2fa_messages(self):
        """Should redirect to 2fa setup."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()

        resp = self.client.post(
            reverse("account_login"),
            {"login": "john", "password": "doe"},
            follow=True,
        )

        # The user is redirected to the 2FA setup page.
        self.assertRedirects(
            resp, reverse("two-factor-setup"), fetch_redirect_response=False
        )


class TestQRCodeGeneration(TestCase):
    """Tests for QR code generation via file or data: protocol."""

    def tearDown(self):
        """Reset settings to default."""
        setattr(app_settings, "QRCODE_TYPE", "data")

    def test_2fa_setup_data(self):
        """Test 2FA setup using 'data:' protocol."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        self.client.post(reverse("account_login"), {"login": "john", "password": "doe"})
        resp = self.client.get(reverse("two-factor-setup"))

        self.assertContains(resp, "data:image/svg+xml;base64,")

    @patchfs
    def test_2fa_setup_file(self, fs):
        """Test 2FA setup using an SVG file."""
        # Create the fake qrcodes directory.
        fs.create_dir("qrcodes")

        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        setattr(app_settings, "QRCODE_TYPE", "file")
        self.client.post(reverse("account_login"), {"login": "john", "password": "doe"})
        resp = self.client.get(reverse("two-factor-setup"))

        # This could use a regular expression matching
        # ``qrcodes/[a-f0-9]{32}\.svg``.
        self.assertContains(resp, ".svg")

    def test_2fa_setup_file_no_dir(self):
        """Test 2FA setup using an SVG file without the qr code directory."""
        user = get_user_model().objects.create(username="john")
        user.set_password("doe")
        user.save()
        setattr(app_settings, "QRCODE_TYPE", "file")
        self.client.post(
            reverse("account_login"),
            {
                "login": "john",
                "password": "doe",
            },
        )

        self.assertRaises(
            ImproperlyConfigured,
            self.client.get,
            reverse("two-factor-setup"),
        )
