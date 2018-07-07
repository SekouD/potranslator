#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `potranslator` package."""

import pytest
import sys
import os
import re
from textwrap import dedent
from os.path import isfile, join, getmtime
from os import remove

from click.testing import CliRunner


runner = CliRunner()

from path import Path as path

from potranslator import PoTranslator
from potranslator import commands


is_appveyor = 'APPVEYOR' in os.environ
is_travis = 'TRAVIS' in os.environ
is_CI = is_travis or is_appveyor
is_python2 = sys.version_info < (3, 0)
__dir__ = path(os.path.dirname('./tests/'))


@pytest.fixture(scope="function")
def temp_test_data(request, tmpdir):
    template_dir = 'test_data'

    tmpdir = path(tmpdir)
    (__dir__ / template_dir).copytree(tmpdir / template_dir)
    cwd = os.getcwd()
    temp = tmpdir / template_dir
    os.chdir(temp)

    def fin():
        os.chdir(cwd)
    request.addfinalizer(fin)
    return temp


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


@pytest.fixture(scope="function")
def home_in_temp(request, tmpdir):
    """change HOME environment variable to temporary location

     To avoid real .transifexrc will be rewritten.
     """
    home = os.environ.get('HOME')
    os.environ['HOME'] = tmpdir.strpath

    def fin():
        del os.environ['HOME']
        if home:
            os.environ['HOME'] = home
    request.addfinalizer(fin)
    return tmpdir


class TestPoTranslator:
    test_languages = ('es', 'fr', 'it', 'pt', 'ro')

    def test_failed_translate_unsupported_language(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        test_po_file = './empty_test.po'
        with pytest.raises(ValueError):
            failed_translation = translator.translate(test_po_file, 'sp')
        return

    def test_failed_translate_auto_detect(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        test_po_file = './empty_test.po'
        with pytest.raises(ValueError):
            failed_translation = translator.translate(test_po_file)
        return

    def test_translate(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        test_po_file = './empty_test.po'
        translation, updated = translator.translate(test_po_file, 'es')
        assert all([entry.msgstr != '' for entry in translation])
        if not is_python2:
            assert translation[0].msgstr == 'Créditos'
        else:
            assert translation[0].msgstr.encode('utf-8') == 'Créditos'
        return

    def test_translate_auto_save(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        test_po_file = './empty_test.po'
        modif_time = getmtime(test_po_file)
        translation, updated = translator.translate(test_po_file, 'es', auto_save=True)
        last_modif_time = getmtime(test_po_file)
        assert modif_time < last_modif_time
        return

    def test_translate_all_locale(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        translations = translator.translate_all_locale()
        assert not 'sp' in translations
        assert all(k in translations for k in self.test_languages)
        assert all('authors.po' in k for k in list(translations.values()))
        if not is_python2:
            assert translations['es']['authors.po'][0].msgstr == 'Créditos'
        else:
            assert translations['es']['authors.po'][0].msgstr.encode('utf-8') == 'Créditos'
        return

    def test_translate_from_pot(self, temp_test_data):
        """

        :return:
        """
        status = {
            'created': 0,
            'updated': 0,
            'not_changed': 0,
        }
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        test_pot_file = './test_pot_files/test-usage.pot'
        translations = translator.translate_from_pot(test_pot_file, status, target_langs=self.test_languages)
        assert all(k in translations for k in self.test_languages)
        if not is_python2:
            assert translations['es'][0].msgstr == 'Uso'
        else:
            assert translations['es'][0].msgstr.encode('utf-8') == 'Uso'
        assert isfile(join(translator.locale_dir, '/'.join(('es', 'LC_MESSAGES', 'test-usage.po'))))
        return

    def test_translate_all_pot(self, temp_test_data):
        """

        :return:
        """
        translator = PoTranslator(pot_dir='./test_pot_files', locale_dir='./locale')
        translations = translator.translate_all_pot(target_langs=self.test_languages)
        assert all(k in translations['test-authors.pot'] for k in self.test_languages)
        assert all(k in translations['test-usage.pot'] for k in self.test_languages)

        if not is_python2:
            assert translations['test-authors.pot']['es'][0].msgstr == 'Créditos'
        else:
            assert translations['test-authors.pot']['es'][0].msgstr.encode('utf-8') == 'Créditos'
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
        return

    def test_update_pot_notfound(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale'])
        assert r1.exit_code != 0
        assert 'Please specify a pot directory with -p option,' in r1.output
        return

    def test_update_no_language(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale'])
        assert r1.exit_code != 0
        assert 'No languages were found. Please specify a language with -l' in r1.output
        return

    def test_update_simple(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0
        return

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
        return

    def test_update_with_conf_file(self, temp):
        r1 = runner.invoke(commands.main, ['-c', './conf.py', 'update', '-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0
        assert 'Created: README.po' in r1.output
        assert 'Updated: README.po' in r1.output
        assert 'ja/LC_MESSAGES/README.po' in r1.output
        return


    def test_stat(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja'])
        assert r1.exit_code == 0

        r2 = runner.invoke(commands.stat, ['-d', 'locale'])
        assert r2.exit_code == 0
        assert 'README.po: 1 translated, 0 fuzzy, 0 untranslated.' in r2.output
        return

    def test_stat_with_multiple_languages(self, temp):
        r1 = runner.invoke(commands.update, ['-d', 'locale', '-p', '_build/locale', '-l', 'ja,de,it'])
        assert r1.exit_code == 0

        # r2 = runner.invoke(commands.stat, ['-d', 'locale', '-l', 'ja,de', '-l', 'it'])
        r2 = runner.invoke(commands.stat, ['-d', 'locale', '-l', 'ja'])
        assert r2.exit_code == 0
        assert 'README.po: 1 translated, 0 fuzzy, 0 untranslated.' in r2.output
        return

    def test_build(self, temp):
        result = runner.invoke(commands.build, ['--locale-dir', 'locale'])
        assert result.exit_code == 0
        return


class TestTransifexCMD:
    def test_create_transifexrc(self, home_in_temp):
        r1 = runner.invoke(commands.main,
                           [
                               'create-transifexrc',
                               '--transifex-username', 'spam-id',
                               '--transifex-password', 'egg-pw',
                           ])
        assert r1.exit_code == 0
        return

    def test_create_txconfig(self, home_in_temp, temp):
        r1 = runner.invoke(commands.main, ['create-txconfig'])
        assert r1.exit_code == 0
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources(self, home_in_temp, temp):
        r1 = runner.invoke(commands.main, ['create-txconfig'])
        assert r1.exit_code == 0
        r2 = runner.invoke(commands.update_txconfig_resources,
                           [
                               '--transifex-project-name', 'ham-project',
                               '-d', 'locale',
                           ])
        assert r2.exit_code == 0
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources_with_config(self, home_in_temp, temp):
        tx_dir = temp / '.tx'
        tx_dir.makedirs()
        (tx_dir / 'config').write_text(dedent("""\
        [main]
        host = https://www.transifex.com

        [ham-project.domain1]
        """))

        (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

        r1 = runner.invoke(commands.main, ['update-txconfig-resources', '-d', 'locale'])
        assert r1.exit_code == 0

        data = (tx_dir / 'config').text()
        assert re.search(r'\[ham-project\.README\]', data)
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources_with_pot_dir_argument(self, home_in_temp, temp):
        tx_dir = temp / '.tx'
        tx_dir.makedirs()
        (tx_dir / 'config').write_text(dedent("""\
        [main]
        host = https://www.transifex.com

        [ham-project.domain1]
        """))

        r1 = runner.invoke(commands.main,
                           ['update-txconfig-resources',
                            '-d', 'locale',
                            '-p', '_build/locale',
                            ])
        assert r1.exit_code == 0

        data = (tx_dir / 'config').text().replace('\\', '/')
        assert re.search(r'\[ham-project\.README\]', data)
        assert re.search(r'source_file = _build/locale/README.pot', data)
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources_with_project_name_including_dots(self, home_in_temp, temp):
        tx_dir = temp / '.tx'
        tx_dir.makedirs()
        (tx_dir / 'config').write_text(dedent("""\
        [main]
        host = https://www.transifex.com
        """))

        (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

        r1 = runner.invoke(commands.main,
                           ['update-txconfig-resources',
                            '-d', 'locale',
                            '--transifex-project-name', 'ham-project.com',
                            ])
        assert r1.exit_code == 0

        data = (tx_dir / 'config').text()
        assert re.search(r'\[ham-projectcom\.README\]', data)
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources_with_project_name_including_spaces(self, home_in_temp, temp):
        tx_dir = temp / '.tx'
        tx_dir.makedirs()
        (tx_dir / 'config').write_text(dedent("""\
        [main]
        host = https://www.transifex.com
        """))

        (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

        r1 = runner.invoke(commands.main,
                           ['update-txconfig-resources',
                            '-d', 'locale',
                            '--transifex-project-name', 'ham project com',
                            ])
        assert r1.exit_code == 0

        data = (tx_dir / 'config').text()
        assert re.search(r'\[ham-project-com\.README\]', data)
        return

    @pytest.mark.skipif(is_CI, reason="Temp folder shenanigans.")
    def test_update_txconfig_resources_with_potfile_including_symbols(self, home_in_temp, temp):
        tx_dir = temp / '.tx'
        tx_dir.makedirs()
        (tx_dir / 'config').write_text(dedent("""\
        [main]
        host = https://www.transifex.com
        """))

        (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

        # copy README.pot to 'example document.pot'
        readme = (temp / '_build' / 'locale' / 'README.pot').text()
        (temp / '_build' / 'locale' / 'example document.pot').write_text(readme)

        # copy README.pot to 'test.document.pot'
        (temp / '_build' / 'locale' / 'test.document.pot').write_text(readme)

        r1 = runner.invoke(commands.main,
                           ['update-txconfig-resources',
                            '-d', 'locale',
                            '--transifex-project-name', 'ham project com',
                            ])
        assert r1.exit_code == 0

        data = (tx_dir / 'config').text()
        assert re.search(r'\[ham-project-com\.example_document\]', data)
        assert re.search(r'\[ham-project-com\.test_document\]', data)
        return
