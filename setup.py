#!/usr/bin/env python
# coding: utf-8

import os.path
import warnings
import sys

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command
from distutils.spawn import spawn

try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print('Cannot import py2exe', file=sys.stderr)
        exit(1)

res_files = [('resources', ['./rubikquat_src/resources/images2.png'])]

py2exe_options = {
    'bundle_files': 3,
    'compressed': 1,
    'optimize': 2,
    'includes': ['numpy', 'pygame'],
    'dist_dir': 'build',
    'dll_excludes': ['w9xpopen.exe', 'crypt32.dll'],
}

# Get the version from rubikquat_src/version.py without importing the package
exec(compile(open('rubikquat_src/version.py').read(),
             'rubikquat_src/version.py', 'exec'))

DESCRIPTION = 'RubikQuat'
LONG_DESCRIPTION = 'Rubik 3D-Simulator using Pygame and Quaternions'

py2exe_console = [{
    'script': './rubikquat_src/__main__.py',
    'dest_base': 'rubikquat',
    'version': __version__,
    'description': DESCRIPTION,
    'comments': LONG_DESCRIPTION,
    'product_name': 'RubikQuat',
    'product_version': __version__,
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {'py2exe': py2exe_options},
    'zipfile': None
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params

setup(
    name='RubikQuat',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/igor-marinescu/RubikQuat',
    author='Igor Marinescu',
    author_email='igor.marinescu@gmail.com',
    maintainer='Igor Marinescu',
    maintainer_email='igor.marinescu@gmail.com',
    license='GNU GPL3',
    
    data_files = res_files,
    packages=['rubikquat_src'],

    classifiers=[
        'Topic :: Education',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    **params
)
