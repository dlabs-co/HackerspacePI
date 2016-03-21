#!/usr/bin/env python3
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='hackerspacepi',
    version='0.1.4',
    description="SpaceAPI compliant service written in python3.5",
    long_description="SpaceAPI compliant service written in python3.5",
    author="David Francos Cuartero",
    author_email='me@davidfrancos.net',
    url='https://github.com/XayOn/HackerspacePI',
    packages=[
        'hackerspacepi',
    ],
    package_dir={'hackerspacepi':
                 'hackerspacepi'},
    entry_points={
        'console_scripts':
        ['hackerspacepi=hackerspacepi:server',
        'hackerspacepi_client=hackerspacepi:client']
    },

    include_package_data=True,
    install_requires=["aiohttp"],
    license="BSD",
    zip_safe=False,
    keywords='hackerspacepi',
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
)
