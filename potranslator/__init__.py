# -*- coding: utf-8 -*-

"""Top-level package for potranslator."""

__author__ = """SekouD"""
__email__ = 'sekoud.python@gmail.com'
__version__ = '0.1.0'

import json
import polib
from googletrans import Translator
import pkg_resources

from .potranslator import PoTranslator
