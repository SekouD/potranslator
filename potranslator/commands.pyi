from typing import Text, Any, Optional, Mapping, Tuple, List, Sequence, Callable, Iterable, Dict
from .polib import POFile

import click

ENVVAR_PREFIX: Text
TAGS: Tags


def main(ctx: Any,
         config: Any,
         tag: Any
         ) -> None: ...

def update(locale_dir: Text,
           pot_dir: Text,
           language: Text
           ) -> None: ...

def build(locale_dir: Text,
           pot_dir: Text,
           language: Text
          ) -> None: ...

def stat(locale_dir: Text,
         language: Text
         ) -> None: ...

def create_transifexrc(transifex_username: Text,
                       transifex_password: Text
                       ) -> None: ...

def create_txconfig() -> None: ...

def update_txconfig_resources(transifex_project_name: Text,
                              locale_dir: Text,
                              pot_dir: Text
                              ) -> None: ...

def read_config(path: Text,
                passed_tags: Sequence[Text]
                ) -> Mapping[Text, Text]: ...

def get_lang_dirs(path: Text) -> Tuple[Tuple[List[Text]]]: ...


option_locale_dir: Callable
option_pot_dir: Callable
option_output_dir: Callable
option_tag: Callable
option_language: Callable
option_transifex_username: Callable
option_transifex_password: Callable
option_transifex_project_name: Callable
CONTEXT_SETTINGS: Mapping[Text, Sequence[Text]]


class Tags(object):
    tags: Dict[Text, bool] = ...
    __contains__: Callable[[Text], bool]

    def __init__(self,
                 tags: Optional[List[Text]] = ...
                 ) -> None: ...

    def __iter__(self) -> Iterable[Mapping[Text, bool]]: ...

    def has(self,
            tag:Text
            ) -> bool: ...

    def add(self,
            tag:Text
            ) -> None: ...

    def remove(self,
            tag:Text
            ) -> None: ...


class LanguagesType(click.ParamType):
    name: Text= ...
    envvar_list_splitter: Text= ...
    def convert(self,
                value: Text,
                param: Any,
                ctx: Any
                ) -> Tuple[Text, Text]: ...

