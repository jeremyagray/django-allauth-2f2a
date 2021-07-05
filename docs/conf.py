# ******************************************************************************
#
# conf.py:  documentation generation settings
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
"""Documentation generation settings."""

# Add any Sphinx extension module names here, as strings.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "django-allauth-2f2a"
copyright = (
    "2016-2021 Víðir Valberg Guðmundsson and Percipient Networks, LLC; 2021,"
    " Jeremy A Gray, FlyQuackSwim"
)
author = (
    "Víðir Valberg Guðmundsson, Percipient Networks;" " Jeremy A Gray, FlyQuackSwim"
)
version = "0.8.1"
release = "0.8.1"
language = None
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False
# html_theme = "sphinx_rtd_theme"
htmlhelp_basename = "django-allauth-2f2adoc"

latex_elements = {}
latex_documents = [
    (
        master_doc,
        "django-allauth-2f2a.tex",
        "django-allauth-2f2a Documentation",
        author,
        "manual",
    ),
]

man_pages = [
    (
        master_doc,
        "django-allauth-2f2a",
        "django-allauth-2f2a Documentation",
        author,
        1,
    ),
]

texinfo_documents = [
    (
        master_doc,
        "django-allauth-2f2a",
        "django-allauth-2f2a Documentation",
        author,
        "django-allauth-2f2a",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}
