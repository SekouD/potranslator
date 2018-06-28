# -*- coding: utf-8 -*-

"""Main module."""

from os import listdir
from os.path import isfile, join
from . import polib, Translator, pkg_resources, json


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
        pass

    def translate(self, file_name, target_lang, src_lang='auto', encoding='utf-8'):
        """

        :param file_name:
        :param target_lang:
        :param src_lang:
        :param encoding:
        """
        po = polib.pofile(file_name, encoding=encoding)
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
        return

    def translate_all_locale(self, src_lang='auto', encoding='utf-8'):
        """

        :param src_lang:
        :param encoding:
        """
        locales = listdir(self.locale_dir)
        for locale in locales:
            po_files = [file for file in listdir(join(self.locale_dir, locale, 'LC_MESSAGES')) if file.endswith('.po')]
            for po_file in po_files:
                path = join(self.locale_dir, locale, 'LC_MESSAGES', po_file)
                self.translate(path, src_lang=src_lang, target_lang=locale, encoding=encoding)
            pass
        return
