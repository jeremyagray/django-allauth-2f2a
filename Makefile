# ******************************************************************************
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
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

python-modules = allauth_2f2a tests
python-files = manage.py setup.py

.PHONY : test-all
test-all:
	pytest -vvvv --cov allauth_2f2a --cov tests --cov-report term --cov-report html

.PHONY : build
build :
	cd docs && make html
	pip install -q build
	python -m build

.PHONY : clean
clean :
	rm -rf build
	rm -rf dist
	rm -rf django_allauth_2f2a.egg-info
	cd docs && make clean

.PHONY : dist
dist : clean build

.PHONY : commit
commit :
	pre-commit run --all-files

.PHONY : lint
lint :
	black --check --diff $(python-modules) $(python-files)
	isort --check --diff $(python-modules) $(python-files) || exit 0
	flake8 allauth_2f2a tests manage.py setup.py

.PHONY : lint-fix
lint-fix :
	black $(python-modules) $(python-files)
	isort $(python-modules) $(python-files) || exit 0

.PHONY : pip
pip :
	pip install -r requirements.txt

.PHONY : test
test:
	pytest --cov allauth_2f2a --cov tests --cov-report term

.PHONY : upload
upload:
	python3 -m twine upload --verbose dist/*

.PHONY : upload-test
upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*

requirements.txt: poetry.lock
	./freeze.sh > $(@)
