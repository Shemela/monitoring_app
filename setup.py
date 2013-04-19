#!/usr/bin/env python
# coding: utf-8
import os

from setuptools import setup, find_packages


def extract_version():
    """Extract server version."""
    with open(os.path.join('monitoring', '__init__.py')) as f:
        line = f.readline()
        while not line.startswith("__version__"):
            line = f.readline()
    d = {}
    exec(line, d)
    version = d['__version__']
    return version


setup(
    name='monitoring',
    version=extract_version(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    )
