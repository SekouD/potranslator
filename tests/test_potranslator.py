#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `potranslator` package."""

import pytest
import sys
import os
from os.path import isfile, join, getmtime
from os import remove

from click.testing import CliRunner


runner = CliRunner()

from path import Path as path

from potranslator import PoTranslator
from potranslator import commands


is_python2 = sys.version_info < (3, 0)
__dir__ = path(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def temp(request, tmpdir):
    template_dir = 'root'

    tmpdir = path(tmpdir)
    (__dir__ / template_dir).copytree(tmpdir / template_dir)
    cwd = os.getcwd()
    temp = tmpdir / template_dir
    os.chdir(temp)

    def fin():
        os.chdir(cwd)
    request.addfinalizer(fin)
    return temp


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
        translation, updated = self.translator.translate(self.test_po_file, 'es')
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
        translation, updated = self.translator.translate(self.test_po_file, 'es', auto_save=True)
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
        status = {
            'created': 0,
            'updated': 0,
            'not_changed': 0,
        }
        translations = self.translator.translate_from_pot(self.test_pot_file, status, target_langs=self.test_languages)
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


class TestCommandLine:
    def test_command_line_interface(self):
        """Test the CLI."""
        result = runner.invoke(commands.main)
        assert result.exit_code == 0
        assert 'POTRANSLATOR_<UPPER_LONG_NAME>' in result.output
        help_result = runner.invoke(commands.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'All command-line options can be set' in help_result.output

    def test_update_pot_notfound(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale'])
        assert r1.exit_code != 0
        assert 'Please specify a pot directory with -p option,' in r1.output

    def test_update_no_language(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale'])
        assert r1.exit_code != 0
        assert 'No languages were found. Please specify a language with -l' in r1.output

    def test_update_simple(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0

    def test_update_difference_detect(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0
        assert r1.output.count('Created:') == 1
        assert r1.output.count('Updated:') == 1
        assert r1.output.count('Not Changed:') == 0

        with open('_build/locale/README.pot', 'a') as f:
            f.write('\nmsgid "test1"\nmsgstr ""\n')

        r2 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale'])
        assert r2.exit_code == 0
        assert r2.output.count('Created:') == 0
        assert r2.output.count('Updated:') == 0
        assert r2.output.count('Not Changed:') == 1

        with open('_build/locale/README.pot', 'r') as f:
            d = f.read()
            d = d.replace('test1', 'test2')
        with open('_build/locale/README.pot', 'w') as f:
            f.write(d)

        r3 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale'])
        assert r3.exit_code == 0
        assert r3.output.count('Create:') == 0
        assert r3.output.count('Update:') == 0
        assert r3.output.count('Not Changed:') == 1

        r4 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale'])
        assert r4.exit_code == 0
        assert r4.output.count('Create:') == 0
        assert r4.output.count('Update:') == 0
        assert r4.output.count('Not Changed:') == 1

    def test_stat(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0

        r2 = runner.invoke(commands.stat, ['-d', 'locale'])
        assert r2.exit_code == 0
        assert 'README.po: 1 translated, 0 fuzzy, 0 untranslated.' in r2.output

    def test_stat_with_multiple_languages(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja,de,it'])
        assert r1.exit_code == 0

        # r2 = runner.invoke(commands.stat, ['-d', 'locale', '-l', 'ja,de', '-l', 'it'])
        r2 = runner.invoke(commands.stat, ['-d', 'locale', '-l', 'ja'])
        assert r2.exit_code == 0
        assert 'README.po: 1 translated, 0 fuzzy, 0 untranslated.' in r2.output

    def test_build(self, temp):
        result = runner.invoke(commands.build, ['--locale-dir', 'locale'])
        assert result.exit_code == 0
