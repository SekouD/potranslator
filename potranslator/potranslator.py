# -*- coding: utf-8 -*-

"""Main module."""

from os import listdir, makedirs
from os.path import isfile, join, exists
from . import polib, Translator, json
from . import SUPPORTED_LANGUAGES, __version__
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from codecs import open
import sys
import click

try:
    from json.decoder import JSONDecodeError
except ImportError:
    pass

_RESOURCE_PACKAGE = __name__

is_python2 = sys.version_info < (3, 0)




class PoTranslator:
    """
    This is the main class of this library. This class manages all translation tasks.

    :param pot_dir: string.
        Path to the pot directory.
    :param locale_dir: string.
        Path to the locale directory.
    """
    def __init__(self, pot_dir=None, locale_dir=None):
        self.pot_dir = pot_dir
        self.locale_dir = locale_dir
        self.translator = Translator()
        return

    def translate(self, file_name, target_lang='auto', src_lang='auto', encoding='utf-8', auto_save=False, compiled=False):
        """
        Translates the given po file in the specified target language.

        :param file_name: string.
            Path to the filename of the file to translate.
        :param target_lang: string.
            Target language for translation.
        :param src_lang: string.
            Source language for translation.
        :param encoding: string.
            Encoding for saving the po files.
        :param auto_save: bool.
            Toggles auto save feature.
        :param compiled: bool.
            Toggles compilation to mo files.
        :return: tuple.
            A tuple containing the translated version of the original catalog and the status of the POFile.
        """
        po = polib.pofile(file_name, **{'encoding': encoding})
        if target_lang == 'auto':
            try:
                target_lang = po.metadata['Language']
            except KeyError:
                raise ValueError(_('potranslator could not auto-detect the desired translation language for the file {0}.\nPlease provide a target language.').format(file_name))
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(_('Unsupported language.'))
        untranslated = [elmt for elmt in po if elmt.msgstr == '' and not elmt.obsolete]
        if untranslated:
            updated = True
            try:
                translations = self.translator.translate([elmt.msgid for elmt in untranslated], src=src_lang, dest=target_lang)
                for entry, translation in zip(untranslated, translations):
                    entry.msgstr = translation.text
                po.metadata['Translated-By'] = 'potranslator {0}'.format(__version__)
                po.metadata['Last-Translator'] = 'potranslator {0}'.format(__version__)
                po.metadata['Language'] = target_lang
                po.metadata['PO-Revision-Date'] = str(datetime.today())
                print(_('{0} translations for the file {1} have been succesfully retrieved').format(SUPPORTED_LANGUAGES[target_lang], file_name))
            except JSONDecodeError as e:
                print(_('{0} translations for the file {1} could not be retrieved').format(SUPPORTED_LANGUAGES[target_lang], file_name))
            if auto_save:
                po.save(file_name)
                print(_('The file {1} has been succesfully translated in {0} and saved.').format(SUPPORTED_LANGUAGES[target_lang], file_name))
            else:
                print(_('The file {1} has been succesfully translated in {0}.').format(SUPPORTED_LANGUAGES[target_lang], file_name))
            if compiled:
                po.save_as_mofile(file_name.replace('.po', '.mo'))
        else:
            updated = False
        return po, updated

    def translate_all_locale(self, src_lang='auto', encoding='utf-8', auto_save=False, compiled=False):
        """
        Translates all the po files in the found languages in the locale folder.

        :param src_lang: string.
            Source language for translation.
        :param encoding: string.
            Encoding for saving the po files.
        :param auto_save: bool.
            Toggles auto save feature.
        :param compiled: bool.
            Toggles compilation to mo files.
        :return: Dictionary.
            A dictionary of po files.
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
                results[locale][po_file], updated = self.translate(path, src_lang=src_lang, target_lang=locale, encoding=encoding, auto_save=auto_save, compiled=compiled)
        return results

    def translate_from_pot(self, filename, status, target_langs, src_lang='auto', encoding='utf-8', auto_save=False, compiled=False):
        """
        Translates the given pot file in the specified target languages.

        :param filename: string.
            Path to the filename of the file to translate.
        :param target_langs: sequence of strings.
            Target language for translation.
        :param src_lang: string.
            Source language for translation.
        :param encoding: string.
            Encoding for saving the po files.
        :param auto_save: bool.
            Toggles auto save feature.
        :param compiled: bool.
            Toggles compilation to mo files.
        :return: Dictionary.
            A dictionary of po files.
        """
        pot = polib.pofile(filename, **{'encoding': encoding})
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
                status['created'] += 1
                click.echo('Created: {0}'.format(po_file_name))
            results[target_lang], updated = self.translate(po_path, target_lang=target_lang, src_lang=src_lang, encoding=encoding, auto_save=auto_save, compiled=compiled)
            if updated:
                status['updated'] += 1
                click.echo('Updated: {0}'.format(po_file_name))
            else:
                status['not_changed'] +=1
                click.echo('Not Changed: {0}'.format(po_file_name))
        return results

    def translate_all_pot(self, target_langs, src_lang='auto', encoding='utf-8', auto_save=False, compiled=False):
        """
        Translates all the pot files in the pot folder in the specified target languages.

        :param target_langs: sequence of strings.
            Target language for translation.
        :param src_lang: string.
            Source language for translation.
        :param encoding: string.
            Encoding for saving the po files.
        :param auto_save: bool.
            Toggles auto save feature.
        :param compiled: bool.
            Toggles compilation to mo files.
        :return: Dictionary.
            A dictionary of po files.
        """
        pot_files = [file for file in listdir(self.pot_dir) if file.endswith('.pot')]
        results = {}
        status = {
            'created': 0,
            'updated': 0,
            'not_changed': 0,
        }
        for pot_file in pot_files:
            path = join(self.pot_dir, pot_file)
            results[pot_file] = self.translate_from_pot(path, status, target_langs=target_langs, src_lang=src_lang, encoding=encoding, auto_save=auto_save, compiled=compiled)
        return results
