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
