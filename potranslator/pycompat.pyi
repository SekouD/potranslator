from typing import Text, Any, Optional, Mapping, Tuple, List, Sequence, Callable, Iterable, Dict

FS_ENCODING: Text
convert_with_2to3: Optional[Text]


def execfile_(filepath: Text,
              _globals:Mapping
              ) -> None: ...

def relpath(path: Text,
            start: Text) -> Text: ...
