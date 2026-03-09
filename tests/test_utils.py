from __future__ import annotations
from typing import List, Any

from aiogram_dialog.utils import is_list_of


def test_is_list_of() -> None:

    class A:
        pass

    class B:
        pass

    list_true: List[A] = [A(), A()]
    list_false: List[Any] = [A(), B()]

    assert is_list_of(list_true, A) is True
    assert is_list_of(list_false, A) is False
