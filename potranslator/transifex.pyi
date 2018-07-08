from typing import Text, Any, Optional, Mapping, Tuple, List, Sequence, Callable, Iterable, Dict


IGNORED_RESOURCE_NAMES: Tuple[Text,]
TRANSIFEXRC_TEMPLATE: Text
TXCONFIG_TEMPLATE: Text


def get_tx_root() -> Text: ...

def normalize_resource_name(name: Text
                            ) -> Text: ...

def create_transifexrc(transifex_username: Text,
                       transifex_password: Text
                       ) -> None: ...

def create_txconfig() -> None: ...

def update_txconfig_resources(transifex_project_name: Text,
                              locale_dir: Text,
                              pot_dir: Text
                              ) -> None: ...
