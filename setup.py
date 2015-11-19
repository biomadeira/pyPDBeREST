#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pyPDBeREST: A wrapper for the PDBe REST API.
    Copyright (C) 2015  Fábio Madeira

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from setuptools import setup
from setuptools import find_packages

__author__ = 'Fábio Madeira'
__email__ = 'fabiomadeira@me.com'
__version__ = '0.1.0'

setup(
    # Basic package information.
    name='pypdberest',
    version=__version__,
    packages=find_packages(),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['requests>=2.7.0', 'responses'],

    # tests
    test_suite="tests.test_pdberest",

    # Metadata for PyPI.
    author=__author__,
    author_email=__email__,
    license='MIT',
    url='http://github.com/biomadeira/pypdberest/tree/master',
    keywords='pdbe rest api json python',
    description='A python wrapper for the PDBe REST API.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: PyPy3',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering :: Bio-informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

