# ******************************************************************************
#
# utils.py:  utilities for allauth_2f2a
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
"""Utilities for allauth_2f2a."""

import importlib
from base64 import b32encode
from io import BytesIO
from urllib.parse import quote
from urllib.parse import urlencode

import qrcode
from django.contrib.sites.shortcuts import get_current_site
from qrcode.image.svg import SvgPathImage


def generate_totp_config_svg(device, issuer, label):
    """Generate a TOTP configuration SVG.

    Returns
    -------
    io.BytesIO
        SVG image as a memory-based file.
    """
    params = {
        "secret": b32encode(device.bin_key).decode("utf-8"),
        "algorithm": "SHA1",
        "digits": device.digits,
        "period": device.step,
        "issuer": issuer,
    }

    otpauth_url = "otpauth://totp/{label}?{query}".format(
        label=quote(label),
        query=urlencode(params),
    )

    img = qrcode.make(otpauth_url, image_factory=SvgPathImage)
    io = BytesIO()
    img.save(io)

    return io.getvalue()


def generate_totp_config_svg_for_device(request, device):
    """Generate a TOTP configuration SVG for a device.

    Returns
    -------
    io.BytesIO
        SVG image as a memory-based file.
    """
    issuer = get_current_site(request).name
    label = "{issuer}: {username}".format(
        issuer=issuer,
        username=request.user.get_username(),
    )

    return generate_totp_config_svg(
        device=device,
        issuer=issuer,
        label=label,
    )


def user_has_valid_totp_device(user):
    """Determine if the user has a valid TOTP device.

    Parameters
    ----------
    user
        The current Django user object.

    Returns
    -------
    boolean
        ``True`` if ``user`` has a valid TOTP device, ``False``
        otherwise.
    """
    if not user.is_authenticated:
        return False

    return user.totpdevice_set.filter(confirmed=True).exists()


# Idea and code borrowed from django-alluth form configuration.
def import_attribute(path):
    """Import an attribute given its string path."""
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def get_form_class(forms, form_id, default_form):
    """Return a form class."""
    form_class = forms.get(form_id, default_form)
    if isinstance(form_class, str):
        form_class = import_attribute(form_class)
    return form_class
