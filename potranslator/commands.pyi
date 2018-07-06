from typing import Text, Any, Optional, Mapping, Tuple, List, Sequence, Callable, Iterable, Dict
from .polib import POFile

import click

ENVVAR_PREFIX: Text


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


def read_config(path: Text,
                passed_tags: Sequence[Text]
                ) -> Mapping[Text, Text]: ...

def get_lang_dirs(path: Text) -> Tuple[Tuple[List[Text]]]: ...

class LanguagesType(click.ParamType):
    name: Text= ...
    envvar_list_splitter: Text= ...

