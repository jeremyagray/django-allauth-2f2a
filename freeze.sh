#!/bin/bash

pip='/home/gray/.virtualenvs/django-allauth-2f2a/bin/pip'
sed='/usr/bin/sed'

${pip} freeze | ${sed} 's/ @ .*-\(.*\)\(-py[23]\|-cp39-cp39\|-cp36\|\.tar\).*$/==\1/' | ${sed} 's/^django-\(blog\|products\) .*$/git+file:\/\/\/home\/gray\/src\/git\/django-\1.git/'
