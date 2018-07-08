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
                'path.py==11.0.1',
                'importlib_resources==1.0.1',
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
                     'importlib_resources==1.0.1',
                     ]

extras_require = {
    'transifex': [
        'transifex_client>=0.13.4'
    ],
}

setup(
    version='1.1.0',
    author="SekouD",
    author_email='sekoud.python@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Natural Language :: Afrikaans', 'Natural Language :: Arabic','Natural Language :: German',
        'Natural Language :: Greek', 'Natural Language :: English', 'Natural Language :: French',
        'Natural Language :: Italian', 'Natural Language :: Japanese',
        'Natural Language :: Chinese (Simplified)',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A python package to easily translate po and pot files in any language supported by Google Translate.",
    entry_points={
        'console_scripts': [
            'potranslator=potranslator.commands:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    package_data={'translations': ['potranslator/locale_dir/*'],
                  'tests': ['tests/*'],
                  'type_stubs': ['potranslator/py.typed', 'potranslator/*']},
    keywords='potranslator sphinx sphinx-intl gettext localization translation translate po pot mo internationalization python google',
    name='potranslator',
    packages=find_packages(include=['potranslator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SekouD/potranslator',
    zip_safe=False,
)
