# -*- coding: utf-8 -*-

"""Top-level package for potranslator."""

__author__ = """SekouD"""
__email__ = 'sekoud.python@gmail.com'
__version__ = '0.2.0'
__copyright__ = "Copyright (c) 2017, SekouD"
__credits__ = ("SekouD",)
__license__ = "MIT"
__maintainer__ = "SekouD"
__status__ = "Production"

import json
import polib
from googletrans import Translator
import pkg_resources
import platform
from locale import windows_locale, getdefaultlocale
import gettext
import inspect
from codecs import open

# Sets up the automatic translation of annotated strings displayed to the user.
_RESOURCE_PACKAGE = __name__
_TRANSLATIONS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'locale')

json_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'supported_languages.json')

with open(json_file, 'r', encoding='utf-8') as file:
    SUPPORTED_LANGUAGES = json.load(file)

_TRANSLATED_LANGUAGES = [key for key in SUPPORTED_LANGUAGES if key != 'en']


def _get_user_locale():
    """
    | Gets the user locale to set the user interface language language.
    | The default is set to english if the user's system locale is not one of the translated languages.

    :return: string.
        The user locale.

    """
    if 'Windows' in platform.system():
        import ctypes
        windll = ctypes.windll.kernel32
        default_locale = windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        default_locale = getdefaultlocale()
    if default_locale:
        if isinstance(default_locale, tuple):
            user_locale = [0][:2]
        else:
            user_locale = default_locale[:2]
    else:
        user_locale = 'en'
    return user_locale


def _getdoc(object):
    """
    Translates the docstrings of the objects defined in the packeage in the supported languages.

    :param object:
    :return: string.
        The translated version of the object's docstring.
    """
    try:
        doc = object.__doc__
    except AttributeError:
        return None
    if not isinstance(doc, str):
        return None
    return inspect.cleandoc(_(doc))


_user_locale = _get_user_locale()

if _user_locale in _TRANSLATED_LANGUAGES:
    _POTRANSLATOR_TRANSLATIONS = gettext.translation(domain='mlconjug',
                                                localedir=_TRANSLATIONS_PATH,
                                                languages=[_user_locale], fallback=True, codeset='UTF-8')
else:
    _POTRANSLATOR_TRANSLATIONS = gettext.NullTranslations()

_POTRANSLATOR_TRANSLATIONS.install()


# Replaces the getdoc method
inspect.getdoc = _getdoc

from .potranslator import PoTranslator
