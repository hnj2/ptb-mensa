#!/usr/bin/env python3.8

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=['setuptools_scm'],
)
