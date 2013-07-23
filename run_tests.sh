#!/bin/bash

PYTHONPATH=".:$PYTHONPATH"


echo '=== pyflakes ==='
pyflakes ./proptools.py || exit $?
echo 'pyflakes completed.'


echo -e '\n=== Running unittests ==='
coverage run --branch ./proptools.py --verbose
STATUS=$?

echo -e '\n--- Generating Coverage Report ---'
coverage html --include='proptools*'

echo 'Report generated.'

[ "$STATUS" -eq 0 ] || exit $STATUS

exit "$STATUS"
