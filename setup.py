#! /usr/bin/env python

import sys
from setuptools import setup


if 'upload' in sys.argv:
    if '--sign' not in sys.argv and sys.argv[1:] != ['upload', '--help']:
        raise SystemExit('Refusing to upload unsigned packages.')


setup(
    name='proptools',
    description='Property types: LazyProperty, TypedProperty, SetOnceProperty',
    url='https://github.org/nejucomo/proptools',
    license='MIT (see LICENSE.txt)',
    version='0.2.dev0',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    py_modules=['proptools'],
)
