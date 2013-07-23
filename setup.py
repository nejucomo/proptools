#! /usr/bin/env python

import sys
from distutils.core import setup


if 'upload' in sys.argv:
    if '--sign' not in sys.argv and sys.argv[1:] != ['upload', '--help']:
        raise SystemExit('Refusing to upload unsigned packages.')


setup(name = 'proptools',
      description = 'Some property subtypes: LazyProperty, TypedProperty, SetOnceProperty',
      url = 'https://github.org/nejucomo/proptools',
      license = 'GPLv3',
      version = '0.1',
      author = 'Nathan Wilcox',
      author_email = 'nejucomo@gmail.com',
      py_modules = ['proptools'],
      )
