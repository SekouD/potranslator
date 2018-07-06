# -*- coding: utf-8 -*-
"""
    potranslator
    ~~~~~~~~~~~
    Python package to easily translate po and pot files in any language supported by Google Translate.
    Command Line Script adapted from sphinx-intl for compatibility.

    :copyright: Copyright (c) 2018 by SekouD.
    :copyright: Copyright (c) 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import os
from glob import glob

import click

# from . import catalog as c
from .pycompat import relpath
from .potranslator import PoTranslator
from . import polib


# ==================================
# utility functions

def get_lang_dirs(path):
    """

    :param path: unicode.
    :return: tuple.
    """
    dirs = [relpath(d, path)
            for d in glob(path + '/[a-z]*')
            if os.path.isdir(d) and not d.endswith('pot')]
    return (tuple(dirs),)


# ==================================
# commands

def update(locale_dir, pot_dir, languages):
    """
    Update specified language's po files from pot.

    :param unicode locale_dir: path for locale directory
    :param unicode pot_dir: path for pot directory
    :param tuple languages: languages to update po files
    :return: Dict of POFiles.
    :rtype: dict
    """
    translator = PoTranslator(pot_dir=pot_dir, locale_dir=locale_dir)
    results = translator.translate_all_pot(target_langs=languages, auto_save=True)
    return results


def build(locale_dir, output_dir, languages):
    """
    Biuilds specified language's mo files from pot.

    :param unicode locale_dir: path for locale directory
    :param unicode output_dir: path for mo output directory
    :param tuple languages: languages to update po files
    :return: Dict of POFiles.
    :rtype: dict
    """
    translator = PoTranslator(pot_dir=output_dir, locale_dir=locale_dir)
    results = translator.translate_all_pot(target_langs=languages, auto_save=True, compiled=True)
    return results


def stat(locale_dir, languages):
    """
    Print statistics for all po files.

    :param unicode locale_dir: path for locale directory
    :param tuple languages: languages to update po files
    :return: {'FILENAME': {'translated': 0, 'fuzzy': 0, 'untranslated': 0}, ...}
    :rtype: dict
    """
    result = {}

    for lang in languages:
        lang_dir = os.path.join(locale_dir, lang)
        for dirpath, dirnames, filenames in os.walk(lang_dir):
            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                if ext != ".po":
                    continue

                cat = polib.pofile(po_file)
                r = result[po_file.replace('\\', '/')] = {
                    'translated': len(cat.translated_entries()),
                    'fuzzy': len(cat.fuzzy_entries()),
                    'untranslated': len(cat.untranslated_entries()),
                }
                click.echo(
                    '{0}: {1} translated, {2} fuzzy, {3} untranslated.'.format(
                        po_file,
                        r['translated'],
                        r['fuzzy'],
                        r['untranslated'],
                    )
                )

    return result
