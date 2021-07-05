.. *****************************************************************************
..
.. configuration.rst:  basic configuration
..
.. SPDX-License-Identifier: Apache-2.0
..
.. django-allauth-2f2a, a 2fa adapter for django-allauth.
..
.. *****************************************************************************
..
.. Copyright 2016-2021 Víðir Valberg Guðmundsson and Percipient
.. Networks, LLC.
.. Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
..
.. Licensed under the Apache License, Version 2.0 (the "License"); you
.. may not use this file except in compliance with the License.  You
.. may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
.. implied.  See the License for the specific language governing
.. permissions and limitations under the License.
..
.. *****************************************************************************

.. include:: links.rst

===============
 Configuration
===============

``ALLAUTH_2F2A_TEMPLATE_EXTENSION``
===================================

String.  Set the extension for templates used by views of
`django-allauth-2f2a`_.  Defaults to ``ACCOUNT_TEMPLATE_EXTENSION``
from allauth, which is ``html`` by default.

``ALLAUTH_2F2A_ALWAYS_REVEAL_BACKUP_TOKENS``
============================================

Boolean.  Show the remaining backup tokens on the Backup Tokens view
if ``True``.  If ``False``, only show the backup tokens when they are
generated.  Defaults to ``True``.

``ALLAUTH_2F2A_QRCODE_TYPE``
============================

String.  Configure the generation of the QR code image.

Defaults to ``data`` for a base64 encoded SVG image using the 'data:'
protocol.  Setting this to ``file`` will use an SVG file stored in
``settings.MEDIA_ROOT/qrcodes/``.

Use of the 'data:' protocol must be specifically allowed by sites that
are using a strict CSP.  By providing the image as a file, it is
covered by the typical 'self' directives in a strict CSP.  The file is
generated with a UUID4 filename to avoid predictability.  Since all
files are generated in the same directory, a periodic task to remove
all files older than some time can be used to delete old QR codes.

``ALLAUTH_2F2A_2FA_FORMS``
==========================

Dictionary.  Configure the forms uses for the TOTP authentication, TOTP device creation, and TOTP device removal forms.  This allows for subclassing and customization of these forms.  The forms can be then be converted to `django-crispy-forms`_, for example.  The defaults are the original forms.

.. code-block:: python

    ALLAUTH_2F2A_2FA_FORMS = {
        "authentication": "allauth_2f2a.forms.TOTPAuthenticateForm",
        "device": "allauth_2f2a.forms.TOTPDeviceForm",
        "remove": "allauth_2f2a.forms.TOTPDeviceRemoveForm",
    }
