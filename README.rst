.. *****************************************************************************
..
.. README.rst:  project readme
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

=====================
 django-allauth-2f2a
=====================

`django-allauth-2f2a`_ is a port of `django-allauth-2fa`_ that adds
`two-factor authentication`_ to `django-allauth`_ and intends to
continue active development of the code.  The current goals include
generating `SVG`_ codes as files to allow stricter `content security
policies`_, configuration of form classes used by the app to allow
subclassing forms for use with `django-crispy-forms`_, and improved
`CI`_ and testing.

Features
========

* Add `two-factor authentication`_ views and workflow to
  `django-allauth`_.
* Support Authenticator apps via a `QR code`_ when enabling `2FA`_.
* Support single-use back-up codes.

Compatibility
=============

`django-allauth-2f2a`_ will only maintain compatibility with supported
versions of `Django`_ and `python`_ and recent, secure versions of
`django-allauth`_, and `django-otp`_, currently:

* `Python`_ 3.6-3.9.
* `Django`_ 2.2, 3.2.
* `django-allauth`_ 0.44.0 and newer.
* `django-otp`_ 1.0.0 and newer.

Running Tests
=============

Currently, tests can be run using the standard Django testing facility:

.. code-block:: bash

    python manage.py test

or by running tox:

.. code-block:: bash

    tox

Project tests will be moved to pytest in the future.

Running the Test Project
========================

The test project can also be used as a minimal example using the following:

.. code-block:: bash

    # Migrate the SQLite database first.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py migrate
    # Run the server with debug.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py runserver
    # Run the shell.
    DJANGO_SETTINGS_MODULE=tests.settings python manage.py shell

Contributing
============

* Create an issue/pull request.  Check the roadmap for ideas.
* All tox targets should pass.  That includes all tests in all
  supported environments and all the linting checks (black, isort,
  flake8 and flake8-docstrings).
* Test coverage should be 100%.  New features should have new tests.

Roadmap
=======

* implement other OTP/2FA methods in addition to TOTP (see https://github.com/valohai/django-allauth-2fa/issues/23)

  * static
  * HOTP
  * YubiKey
  * Twilio

* clarify code comments
* clarify documentation and improve examples
* publish documentation
* include docstrings in published documentation
* complete meaningful test coverage (make sure the 100% is not just the number)
* generate `SVG`_ codes as files (completed 0.9.0)
* allow configurable form classes (make your forms `crispy`_; completed 0.9.0)
* complete test coverage (completed 0.9.0)
* require `black`_, `flake8-docstrings`_, `pydocstyle`_, `isort`_, `pccc`_, and
  `pre-commit`_ (completed 0.8.1)

Author
======

`django-allauth-2fa`_ was originally created by `Víðir Valberg Guðmundsson (@valberg)`_ of `Percipient Networks`_.  All modifications after the port to `django-allauth-2f2a`_ are created and maintained by `Jeremy A Gray`_ at `FQS`_.

.. _2FA: https://en.wikipedia.org/wiki/Multi-factor_authentication
.. _CI: https://en.wikipedia.org/wiki/Continuous_integration
.. _CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
.. _Django: https://www.djangoproject.com/
.. _FQS: https://www.flyquackswim.com/
.. _Jeremy A Gray: https://github.com/jeremyagray
.. _Percipient Networks: https://www.strongarm.io
.. _Python: https://www.python.org/
.. _QR code: https://en.wikipedia.org/wiki/QR_code
.. _SVG: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
.. _Víðir Valberg Guðmundsson (@valberg): https://github.com/valberg
.. _black: https://github.com/psf/black
.. _content security policies: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
.. _content security policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
.. _crispy: https://github.com/django-crispy-forms/django-crispy-forms/
.. _django-allauth documentation: https://django-allauth.readthedocs.io/en/latest/installation.html
.. _django-allauth-2f2a: https://github.com/jeremyagray/django-allauth-2f2a
.. _django-allauth-2fa: https://github.com/percipient/django-allauth-2fa
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-crispy-forms documentation: https://django-crispy-forms.readthedocs.io/
.. _django-crispy-forms: https://github.com/django-crispy-forms/django-crispy-forms/
.. _django-otp documentation: https://django-otp-official.readthedocs.io/en/latest/overview.html#installation
.. _django-otp: https://github.com/django-otp/django-otp
.. _django: https://www.djangoproject.com/
.. _flake8-docstrings: https://gitlab.com/pycqa/flake8-docstrings
.. _flake8: https://flake8.pycqa.org/
.. _isort: https://pycqa.github.io/isort/
.. _pccc: https://github.com/jeremyagray/pccc/
.. _poetry: https://python-poetry.org/
.. _pre-commit: https://pre-commit.com/
.. _pydocstyle: https://github.com/PyCQA/pydocstyle
.. _pytest: https://pytest.org/
.. _python: https://www.python.org/
.. _qrcode: https://github.com/lincolnloop/python-qrcode
.. _two-factor authentication: https://en.wikipedia.org/wiki/Multi-factor_authentication
