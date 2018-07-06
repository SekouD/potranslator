from typing import Text, Any, Optional, Mapping, Tuple, List, Sequence
from .polib import POFile

def get_lang_dirs(path: Text) -> Tuple[Tuple[List[Text]]]: ...


def update(locale_dir: Text,
           pot_dir: Text,
           languages: Sequence[Text]
           ) -> Mapping[Text, Mapping[Text, Tuple[POFile, bool]]]:...

def build(locale_dir: Text,
          output_dir: Text,
          languages: Sequence[Text]
          ) -> Mapping[Text, Mapping[Text, Tuple[POFile, bool]]]:...

def stat(locale_dir: Text,
         languages: Sequence[Text]
         ) -> Mapping[Text, int]:...
