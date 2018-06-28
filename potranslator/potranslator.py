# -*- coding: utf-8 -*-

"""Main module."""

from os import listdir
from os.path import isfile, join
from . import polib, Translator, pkg_resources, json
from copy import deepcopy


_RESOURCE_PACKAGE = __name__

json_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'supported_languages.json')
with open(json_file, 'r', encoding='utf-8') as file:
    _SUPPORTED_LANGUAGES = json.load(file)


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

    def translate(self, file_name, target_lang='auto', src_lang='auto', encoding='utf-8'):
        """

        :param file_name:
        :param target_lang:
        :param src_lang:
        :param encoding:
        """
        po = polib.pofile(file_name, encoding=encoding)
        if target_lang == 'auto':
            try:
                target_lang = po.metadata['Language']
            except AttributeError:
                raise ValueError('potranslator could not auto-detect the desired translation language for the file {0}.\nPlease provide a target language.'.format(file_name))
        if target_lang not in _SUPPORTED_LANGUAGES:
            raise ValueError('Unsupported language. To see the list of supported languages type potranslator -h')
        untranslated = [elmt for elmt in po if elmt.msgstr == '' and not elmt.obsolete]
        translations = self.translator.translate([elmt.msgid for elmt in untranslated], src=src_lang, dest=target_lang)
        print('{0} translations for the file {1} have been succesfully retrieved'.format(_SUPPORTED_LANGUAGES[target_lang], file_name))
        for entry, translation in zip(untranslated, translations):
            entry.msgstr = translation.text
            pass
        po.save(file_name)
        print('The file {1} has been succesfully translated in {0} and saved.'.format(_SUPPORTED_LANGUAGES[target_lang], file_name))
        return po

    def translate_all_locale(self, src_lang='auto', encoding='utf-8'):
        """

        :param src_lang:
        :param encoding:
        """
        all_locales = listdir(self.locale_dir)
        locales = [locale for locale in all_locales if locale in _SUPPORTED_LANGUAGES]
        unsupported_locales = [locale for locale in all_locales if locale not in _SUPPORTED_LANGUAGES]
        print('Attempting to translate the supported locales:\n{0}'.format(', '.join(locales)))
        if unsupported_locales:
            print('The following locales are not yet supported by potranslator and will not be translated:\n{0}'.format(', '.join(locales)))
        for locale in locales:
            po_files = [file for file in listdir(join(self.locale_dir, locale, 'LC_MESSAGES')) if file.endswith('.po')]
            for po_file in po_files:
                path = join(self.locale_dir, locale, 'LC_MESSAGES', po_file)
                self.translate(path, src_lang=src_lang, target_lang=locale, encoding=encoding)
            pass
        return

    def translate_from_pot(self, filename, target_langs, src_lang='auto', encoding='utf-8'):
        """

        :param filename:
        :param target_langs:
        :param src_lang:
        :param encoding:
        """
        pot = polib.pofile(filename, encoding=encoding)
        for target_lang in target_langs:
            po_file_name = filename.split('/')[-1].split('\\')[-1][:-1]
            po_path = join(self.locale_dir, '/'.join((target_lang, 'LC_MESSAGES', po_file_name)))
            if not isfile(po_path):
                po = deepcopy(pot)
                po.save(po_path)
            self.translate(po_path, target_lang=target_lang, src_lang=src_lang, encoding=encoding)
            pass
        return

    def translate_all_pot(self, target_langs, src_lang='auto', encoding='utf-8'):
        """

        :param target_langs:
        :param src_lang:
        :param encoding:
        """
        pot_files = [file for file in listdir(self.pot_dir) if file.endswith('.pot')]
        for pot_file in pot_files:
            path = join(self.pot_dir, pot_file)
            self.translate_from_pot(path, target_langs=target_langs, src_lang=src_lang, encoding=encoding)
            pass
        return
