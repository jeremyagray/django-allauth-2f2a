.. *****************************************************************************
..
.. installation.rst:  installation directions
..
.. SPDX-License-Identifier: Apache-2.0
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

==============
 Installation
==============

Install `django-allauth-2f2a`_ with pip which will install `Django`_,
`django-allauth`_, `django-otp`_, `qrcode`_ and all of their
requirements.

.. code-block:: bash

    pip install django-allauth-2f2a

Once installed, `django-allauth`_ and `django-otp`_ must be configured
in your `Django`_ settings file.  Please check the `django-allauth
documentation`_ and `django-otp documentation`_ for more in-depth
steps on their configuration.

.. code-block:: python

    INSTALLED_APPS = (
        # Required by allauth.
        'django.contrib.sites',

        # Configure Django auth package.
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',

        # Enable allauth.
        'allauth',
        'allauth.account',

        # Configure the django-otp package.
        'django_otp',
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_static',

        # Enable two-factor auth.
        'allauth_2f2a',
    )

    MIDDLEWARE_CLASSES = (
        # Configure Django auth package.
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        # Configure the django-otp package.  Note this must be after
        # the AuthenticationMiddleware.
        'django_otp.middleware.OTPMiddleware',

        # Reset login flow middleware. If this middleware is included, the login
        # flow is reset if another page is loaded between login and successfully
        # entering two-factor credentials.
        'allauth_2f2a.middleware.AllauthTwoFactorMiddleware',
    )

    # Set the allauth adapter to be the 2FA adapter.
    ACCOUNT_ADAPTER = 'allauth_2f2a.adapter.OTPAdapter'

    # Configure your default site. See
    # https://docs.djangoproject.com/en/dev/ref/settings/#sites.
    SITE_ID = 1

Run the migrations.

.. code-block:: bash

    python manage.py migrate

Include the `django-allauth-2f2a`_ URLs.

.. code-block:: python

    from django.conf.urls import include, url

    urlpatterns = [
        # Include the allauth and 2FA urls from their respective packages.
        url(r'^', include('allauth_2f2a.urls')),
        url(r'^', include('allauth.urls')),
    ]

.. warning::

    Any login view that is *not* provided by `django-allauth`_ will
    bypass the allauth workflow (including two-factor
    authentication). The `Django`_ admin site includes an additional
    login view (usually available at ``/admin/login``).

    The easiest way to fix this is to wrap it in
    ``staff_member_required`` decorator and disallow access to the
    admin site to all, except logged in staff members through allauth
    workflow.  (the code only works if you use the standard admin
    site, if you have a custom admin site you'll need to customize
    this more):

    .. code-block:: python

        from django.contrib import admin
        from django.contrib.admin.views.decorators import staff_member_required

        # Ensure users go through the allauth workflow when logging into admin.
        admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login')
        # Run the standard admin set-up.
        admin.autodiscover()
