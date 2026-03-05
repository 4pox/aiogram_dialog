from __future__ import annotations
from typing import TYPE_CHECKING, Type, List
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from .dialog import Dialog
    from aiogram.filters import Command, StateFilter, Filter


@dataclass
class HandlerConfig:
    type: HandlerType
    filter: Command | StateFilter | Filter | List[Filter]


class HandlerType(Enum):
    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"


class Handler:

    dialog: Type[Dialog] | Dialog

    def __init__(self, dialog: Type[Dialog] | Dialog) -> None:
        self.dialog = dialog
        self.enable_hooks: bool = False
