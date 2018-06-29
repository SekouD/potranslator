# -*- coding: utf-8 -*-

"""Main module."""

from os import listdir, makedirs
from os.path import isfile, join, exists
from . import polib, Translator, pkg_resources, json
from . import SUPPORTED_LANGUAGES, __version__
from collections import defaultdict
from copy import deepcopy
from codecs import open
import sys

_RESOURCE_PACKAGE = __name__

is_python2 = sys.version_info < (3, 0)




class PoTranslator:
    """

    :param pot_dir:
    :param locale_dir:
    """
    def __init__(self, pot_dir=None, locale_dir=None):
        self.pot_dir = pot_dir
        self.locale_dir = locale_dir
        self.translator = Translator()
        return

    def translate(self, file_name, target_lang='auto', src_lang='auto', encoding='utf-8', auto_save=False):
        """


        :param file_name:
        :param target_lang:
        :param src_lang:
        :param encoding:
        :param auto_save:
        :return: POFile.
        """
        po = polib.pofile(file_name, encoding=encoding)
        if target_lang == 'auto':
            try:
                target_lang = po.metadata['Language']
            except KeyError:
                raise ValueError(_('potranslator could not auto-detect the desired translation language for the file {0}.\nPlease provide a target language.').format(file_name))
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(_('Unsupported language. To see the list of supported languages type potranslator -h'))
        untranslated = [elmt for elmt in po if elmt.msgstr == '' and not elmt.obsolete]
        translations = self.translator.translate([elmt.msgid for elmt in untranslated], src=src_lang, dest=target_lang)
        print(_('{0} translations for the file {1} have been succesfully retrieved').format(SUPPORTED_LANGUAGES[target_lang], file_name))
        for entry, translation in zip(untranslated, translations):
            entry.msgstr = translation.text
        po.metadata['Translated-By'] = 'potranslator {0}'.format(__version__)
        if auto_save:
            po.save(file_name)
            print(_('The file {1} has been succesfully translated in {0} and saved.').format(SUPPORTED_LANGUAGES[target_lang], file_name))
        else:
            print(_('The file {1} has been succesfully translated in {0}.').format(SUPPORTED_LANGUAGES[target_lang], file_name))
        return po

    def translate_all_locale(self, src_lang='auto', encoding='utf-8', auto_save=False):
        """

        :param src_lang:
        :param encoding:
        :param auto_save:
        :return: Dictionary.
        """
        all_locales = listdir(self.locale_dir)
        locales = [locale for locale in all_locales if locale in SUPPORTED_LANGUAGES]
        unsupported_locales = [locale for locale in all_locales if locale not in SUPPORTED_LANGUAGES]
        print(_('Attempting to translate the supported locales:\n{0}').format(', '.join(locales)))
        if unsupported_locales:
            print(_('The following locales are not yet supported by potranslator and will not be translated:\n{0}').format(', '.join(locales)))
        results = defaultdict(dict)
        for locale in locales:
            po_files = [file for file in listdir(join(self.locale_dir, locale, 'LC_MESSAGES')) if file.endswith('.po')]
            for po_file in po_files:
                path = join(self.locale_dir, locale, 'LC_MESSAGES', po_file)
                results[locale][po_file] = self.translate(path, src_lang=src_lang, target_lang=locale, encoding=encoding, auto_save=auto_save)
        return results

    def translate_from_pot(self, filename, target_langs, src_lang='auto', encoding='utf-8', auto_save=False):
        """

        :param filename:
        :param target_langs:
        :param src_lang:
        :param encoding:
        :param auto_save:
        :return: Dictionary.
        """
        pot = polib.pofile(filename, encoding=encoding)
        results = {}
        for target_lang in target_langs:
            po_file_name = filename.split('/')[-1].split('\\')[-1][:-1]
            po_path = join(self.locale_dir, '/'.join((target_lang, 'LC_MESSAGES', po_file_name)))
            po_dir = join(self.locale_dir, '/'.join((target_lang, 'LC_MESSAGES')))
            if not isfile(po_path):
                if not exists(po_dir):
                    makedirs(po_dir)
                po = deepcopy(pot)
                po.save(po_path)
            results[target_lang] = self.translate(po_path, target_lang=target_lang, src_lang=src_lang, encoding=encoding, auto_save=auto_save)
        return results

    def translate_all_pot(self, target_langs, src_lang='auto', encoding='utf-8', auto_save=False):
        """

        :param target_langs:
        :param src_lang:
        :param encoding:
        :param auto_save:
        :return: Dictionary.
        """
        pot_files = [file for file in listdir(self.pot_dir) if file.endswith('.pot')]
        results = {}
        for pot_file in pot_files:
            path = join(self.pot_dir, pot_file)
            results[pot_file] = self.translate_from_pot(path, target_langs=target_langs, src_lang=src_lang, encoding=encoding, auto_save=auto_save)
        return results
