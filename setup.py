#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'googletrans==2.3.0',
                'polib==1.1.0',
                ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pip==10.0.1',
                     'pytest==3.6.2',
                     'pytest-runner==4.2',
                     'Click>=6.0',
                     'bump2version==0.5.8',
                     'wheel==0.31.1',
                     'watchdog==0.8.3',
                     'flake8==3.5.0',
                     'tox==3.0.0',
                     'coverage==4.5.1',
                     'Sphinx==1.7.5',
                     'twine==1.11.0',
                     'googletrans==2.3.0',
                     'polib==1.1.0',
                     ]

setup(
    author="SekouD",
    author_email='sekoud.python@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A package to easily translate po and pot files in any language supported by Google Translate.",
    entry_points={
        'console_scripts': [
            'potranslator=potranslator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    package_data={'translations': ['potranslator/locale/*'],
                  'type_stubs': ['potranslator/py.typed', 'potranslator/*']},
    keywords='potranslator',
    name='potranslator',
    packages=find_packages(include=['potranslator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SekouD/potranslator',
    version='0.2.0',
    zip_safe=False,
)
