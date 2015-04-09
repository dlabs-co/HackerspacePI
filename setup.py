#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Flask',
    'flask-sqlalchemy',
    'flask-restless',
    'flask-login',
    'mysql-python',
    'flask-wtf'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='HackerspacePI',
    version='0.1.0',
    description="Hackerspace API with varios sensors for status reporting implemented in Dlabs - Zaragoza's Hackerspace",
    long_description=readme + '\n\n' + history,
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/HackerspacePI',
    packages=[
        'HackerspacePI',
    ],
    package_dir={'HackerspacePI':
                 'HackerspacePI'},
    entry_points={
        'console_scripts':
            ['hackerspacepi=HackerspacePI.HackerspacePI:main']
    },

    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='HackerspacePI',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
