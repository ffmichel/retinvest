#!/usr/bin/env python
import os
import re

import setuptools

PACKAGE_NAME = 'retinvest'
REQUIREMENTS = 'requirements.txt'


def version(package_name=PACKAGE_NAME):
    version_str = None
    regex = re.compile(r'''^__version__ = ['"]([^'"]*)['"]''')
    with open(os.path.join(package_name, '__init__.py')) as f:
        for line in f:
            mo = regex.search(line)
            if mo is not None:
                version_str = mo.group(1)
                break
    if version_str is None:
        raise RuntimeError('Could not find version number')
    return version_str


def install_requires(requirements=REQUIREMENTS):
    with open(requirements) as fh:
        return [line.strip() for line in fh]


setuptools.setup(
    name=PACKAGE_NAME,
    version=version(),
    author='Fabrice Michel',
    packages=setuptools.find_packages(exclude=['scripts']),
    install_requires=install_requires(),
)
