#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `potranslator` package."""

import pytest
import sys
from os.path import isfile, join, getmtime
from os import remove

from click.testing import CliRunner

from potranslator import PoTranslator
from potranslator import cli


is_python2 = sys.version_info < (3, 0)

class TestPoTranslator:
    translator = PoTranslator(pot_dir='./tests/test_data/test_pot_files', locale_dir='./tests/test_data/locale')
    test_po_file = './tests/test_data/empty_test.po'
    test_pot_file = './tests/test_data/test_pot_files/test-usage.pot'
    test_languages = ('es', 'fr', 'it', 'pt', 'ro')

    def test_failed_translate_unsupported_language(self):
        """

        :return:
        """
        with pytest.raises(ValueError):
            failed_translation = self.translator.translate(self.test_po_file, 'sp')
        return

    def test_failed_translate_auto_detect(self):
        """

        :return:
        """
        with pytest.raises(ValueError):
            failed_translation = self.translator.translate(self.test_po_file)
        return

    def test_translate(self):
        """

        :return:
        """
        translation = self.translator.translate(self.test_po_file, 'es')
        assert all([entry.msgstr != '' for entry in translation])
        if not is_python2:
            assert translation[0].msgstr == 'Créditos'
        else:
            assert translation[0].msgstr.encode('utf-8') == 'Créditos'
        return

    def test_translate_auto_save(self):
        """

        :return:
        """
        modif_time = getmtime(self.test_po_file)
        translation = self.translator.translate(self.test_po_file, 'es', auto_save=True)
        last_modif_time = getmtime(self.test_po_file)
        assert modif_time < last_modif_time
        return

    def test_translate_all_locale(self):
        """

        :return:
        """
        translations = self.translator.translate_all_locale()
        assert not 'sp' in translations
        assert all(k in translations for k in self.test_languages)
        assert all('authors.po' in k for k in list(translations.values()))
        if not is_python2:
            assert translations['es']['authors.po'][0].msgstr == 'Créditos'
        else:
            assert translations['es']['authors.po'][0].msgstr.encode('utf-8') == 'Créditos'
        return

    def test_translate_from_pot(self):
        """

        :return:
        """
        translations = self.translator.translate_from_pot(self.test_pot_file, target_langs=self.test_languages)
        assert all(k in translations for k in self.test_languages)
        if not is_python2:
            assert translations['es'][0].msgstr == 'Uso'
        else:
            assert translations['es'][0].msgstr.encode('utf-8') == 'Uso'
        assert isfile(join(self.translator.locale_dir, '/'.join(('es', 'LC_MESSAGES', 'test-usage.po'))))
        for locale in self.test_languages:
            remove(join(self.translator.locale_dir, '/'.join((locale, 'LC_MESSAGES', 'test-usage.po'))))
        return

    def test_translate_all_pot(self):
        """

        :return:
        """
        translations = self.translator.translate_all_pot(target_langs=self.test_languages)
        assert all(k in translations['test-authors.pot'] for k in self.test_languages)
        assert all(k in translations['test-usage.pot'] for k in self.test_languages)

        if not is_python2:
            assert translations['test-authors.pot']['es'][0].msgstr == 'Créditos'
        else:
            assert translations['test-authors.pot']['es'][0].msgstr.encode('utf-8') == 'Créditos'
        for locale in self.test_languages:
            for file in ('test-authors.po', 'test-usage.po'):
                remove(join(self.translator.locale_dir, '/'.join((locale, 'LC_MESSAGES', file))))
        return



def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'potranslator.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
