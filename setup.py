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

extras_require = {
    'transifex': [
        'transifex_client>=0.13.4'
    ],
}

setup(
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
        'Natural Language :: Afrikaans', 'Natural Language :: Amharic', 'Natural Language :: Arabic',
        'Natural Language :: Azeerbaijani', 'Natural Language :: Belarusian', 'Natural Language :: Bulgarian',
        'Natural Language :: Bengali', 'Natural Language :: Bosnian', 'Natural Language :: Catalan',
        'Natural Language :: Cebuano', 'Natural Language :: Corsican', 'Natural Language :: Czech',
        'Natural Language :: Welsh', 'Natural Language :: Danish', 'Natural Language :: German',
        'Natural Language :: Greek', 'Natural Language :: English', 'Natural Language :: Esperanto',
        'Natural Language :: Spanish', 'Natural Language :: Estonian', 'Natural Language :: Basque',
        'Natural Language :: Persian', 'Natural Language :: Finnish', 'Natural Language :: French',
        'Natural Language :: Frisian', 'Natural Language :: Irish', 'Natural Language :: Scots Gaelic',
        'Natural Language :: Galician', 'Natural Language :: Gujarati', 'Natural Language :: Hausa',
        'Natural Language :: Hawaiian', 'Natural Language :: Hindi', 'Natural Language :: Hmong',
        'Natural Language :: Croatian', 'Natural Language :: Haitian Creole', 'Natural Language :: Hungarian',
        'Natural Language :: Armenian', 'Natural Language :: Indonesian', 'Natural Language :: Igbo',
        'Natural Language :: Icelandic', 'Natural Language :: Italian', 'Natural Language :: Hebrew',
        'Natural Language :: Japanese', 'Natural Language :: Javanese', 'Natural Language :: Georgian',
        'Natural Language :: Kazakh', 'Natural Language :: Khmer', 'Natural Language :: Kannada',
        'Natural Language :: Korean', 'Natural Language :: Kurdish', 'Natural Language :: Kyrgyz',
        'Natural Language :: Latin', 'Natural Language :: Luxembourgish', 'Natural Language :: Lao',
        'Natural Language :: Lithuanian', 'Natural Language :: Latvian', 'Natural Language :: Malagasy',
        'Natural Language :: Maori', 'Natural Language :: Macedonian', 'Natural Language :: Malayalam',
        'Natural Language :: Mongolian', 'Natural Language :: Marathi', 'Natural Language :: Malay',
        'Natural Language :: Maltese', 'Natural Language :: Myanmar (Burmese)', 'Natural Language :: Nepali',
        'Natural Language :: Dutch', 'Natural Language :: Norwegian', 'Natural Language :: Nyanja (Chichewa)',
        'Natural Language :: Punjabi', 'Natural Language :: Polish', 'Natural Language :: Pashto',
        'Natural Language :: Portuguese (Portugal, Brazil)', 'Natural Language :: Romanian',
        'Natural Language :: Russian', 'Natural Language :: Sindhi', 'Natural Language :: Sinhala (Sinhalese)',
        'Natural Language :: Slovak', 'Natural Language :: Slovenian', 'Natural Language :: Samoan',
        'Natural Language :: Shona', 'Natural Language :: Somali', 'Natural Language :: Albanian',
        'Natural Language :: Serbian', 'Natural Language :: Sesotho', 'Natural Language :: Sundanese',
        'Natural Language :: Swedish', 'Natural Language :: Swahili', 'Natural Language :: Tamil',
        'Natural Language :: Telugu', 'Natural Language :: Tajik', 'Natural Language :: Thai',
        'Natural Language :: Tagalog (Filipino)', 'Natural Language :: Turkish', 'Natural Language :: Ukrainian',
        'Natural Language :: Urdu', 'Natural Language :: Uzbek', 'Natural Language :: Vietnamese',
        'Natural Language :: Xhosa', 'Natural Language :: Yiddish', 'Natural Language :: Yoruba',
        'Natural Language :: Chinese (Simplified)', 'Natural Language :: Chinese (Traditional)',
        'Natural Language :: Zulu',
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
    package_data={'translations': ['potranslator/locale/*'],
                  'tests': ['tests/*'],
                  'type_stubs': ['potranslator/py.typed', 'potranslator/*']},
    keywords='potranslator',
    name='potranslator sphinx sphinx-intl gettext localization translation translate po pot mo internationalization python google',
    packages=find_packages(include=['potranslator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SekouD/potranslator',
    version='1.0.1',
    zip_safe=False,
)
