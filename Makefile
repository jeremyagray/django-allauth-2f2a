# ******************************************************************************
#
# Makefile:  chore makefile for django-allauth-2f2a
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
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

.PHONY : build clean dist commit lint pip upload upload-test test test-all

test-all:
	pytest -vvvv --cov allauth_2f2a --cov tests --cov-report term --cov-report html

build :
	cd docs && make html
	pip install -q build
	python -m build

clean :
	rm -rf build
	rm -rf dist
	rm -rf django_allauth_2f2a.egg-info
	cd docs && make clean

dist : clean build

commit :
	pre-commit run --all-files

lint :
	black --check allauth_2f2a tests setup.py
	isort --check allauth_2f2a tests setup.py
	flake8 allauth_2f2a tests setup.py

pip :
	pip install -r requirements.txt

test:
	pytest --cov allauth_2f2a --cov tests --cov-report term

upload:
	python3 -m twine upload --verbose dist/*

upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*
