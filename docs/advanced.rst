.. *****************************************************************************
..
.. advanced.rst:  advanced configuration
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

========================
 Advanced Configuration
========================

Require a User to Use `2FA`_
============================

A ``User`` can be forced to use `2FA`_ based on any requirements
(e.g. superusers or being in a particular group). This is implemented
by subclassing the ``allauth_2f2a.middleware.BaseRequire2FAMiddleware``
and implementing the ``require_2fa`` method on it. This middleware
needs to be added to your ``MIDDLEWARE_CLASSES`` setting.

For example, to require a user to be a superuser:

.. code-block:: python

    from allauth_2f2a.middleware import BaseRequire2FAMiddleware

    class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
        def require_2fa(self, request):
            # Superusers are require to have 2FA.
            return request.user.is_superuser

If the user doesn't have `2FA`_ enabled they will be redirected to the
`2FA`_ configuration page and will not be allowed to access (most)
other pages.
