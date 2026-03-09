from __future__ import annotations
from typing import List, Any, Type


def is_list_of(lst: List[Any], item_type: Type) -> bool:
    return isinstance(lst, list) and all(isinstance(i, item_type) for i in lst)
