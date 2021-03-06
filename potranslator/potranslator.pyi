# Stubs for potranslator.potranslator (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Text, Any, Optional, Mapping, Tuple
from googletrans import Translator
from polib import POFile

_RESOURCE_PACKAGE: Text = __name__
is_python2: bool

class PoTranslator:
    pot_dir: Text = ...
    locale_dir: Text = ...
    translator: Translator = ...
    def __init__(self,
                 pot_dir: Optional[Text] = ...,
                 locale_dir: Optional[Text] = ...
                 ) -> None: ...

    def translate(self,
                  file_name: Text,
                  target_lang: Text = ...,
                  src_lang: Text = ...,
                  encoding: Text = ...,
                  auto_save: bool = ...,
                  compiled: bool = ...
                  ) -> Tuple[POFile, bool]: ...

    def translate_all_locale(self,
                             src_lang: Text = ...,
                             encoding: Text = ...,
                             auto_save: bool = ...,
                             compiled: bool = ...
                             ) -> Mapping[Text, Mapping[Text, Tuple[POFile, bool]]]: ...

    def translate_from_pot(self,
                           filename: Any,
                           status: Mapping[Text, int],
                           target_langs: Any,
                           src_lang: Text = ...,
                           encoding: Text = ...,
                           auto_save: bool = ...,
                           compiled: bool = ...
                           ) -> Mapping[Text, Tuple[POFile, bool]]: ...

    def translate_all_pot(self,
                          target_langs: Any,
                          src_lang: Text = ...,
                          encoding: Text = ...,
                          auto_save: bool = ...,
                          compiled: bool = ...
                          ) -> Mapping[Text, Mapping[Text, Tuple[POFile, bool]]]: ...
