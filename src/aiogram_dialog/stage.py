from __future__ import annotations
from typing import Any, Dict, List, TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from .dialog import Dialog
    from .handler import HandlerConfig

from aiogram import Router
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.fsm.state import State
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


@dataclass
class StageKeyboard:
    """Make keyboard.

    Attributes:
        buttons: dict[str, Any]
        is_inline: bool = False
        adjust: int = 2
    """

    buttons: dict[str, Any] | None = None
    is_inline: bool | None = False
    adjust: int | None = 2

    def inline(self) -> InlineKeyboardMarkup | None:
        """Make InlineKeyboard

        Returns:
             InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        if self.buttons:
            for k, v in self.buttons.items():
                builder.add(InlineKeyboardButton(text=k, callback_data=v))
            if self.adjust:
                builder.adjust(self.adjust)
            return builder.as_markup()

    def get_inline_callback(self, key: str, default: str) -> Any | None:
        if self.buttons:
            return self.buttons.get(key, default)

    def replay(self) -> ReplyKeyboardMarkup | None:
        """Make ReplayKeyboard

        Returns:
             ReplyKeyboardMarkup
        """
        builder = ReplyKeyboardBuilder()
        if self.buttons:
            for k in self.buttons.keys():
                builder.add(KeyboardButton(text=k))
            if self.adjust:
                builder.adjust(self.adjust)
            return builder.as_markup(resize_keyboard=True)


@dataclass
class StageMessage:
    message: str
    error: str | None = None
    validate_error: str | None = None


class Validator(ABC):
    @abstractmethod
    async def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        pass


@dataclass
class Stage:
    id: int
    name: str
    state: State | str | None
    handler: HandlerConfig
    keyboard: StageKeyboard | None = None
    message: StageMessage | None = None
    validators: List[Validator] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    _router: Router | None = None
    _dialog_instance: Dialog | None = None

    @property
    def router(self) -> Router | None:
        return self._router

    def _set_router(self, router: Router | None = None) -> None:
        self._router = router

    @property
    def dialog_instance(self) -> Dialog | None:
        return self._dialog_instance

    def _set_dialog_instance(self, dialog_instance: Dialog | None) -> None:
        """Set Dialog class"""
        self._dialog_instance = dialog_instance

    @property
    def next(self) -> Stage | None:
        try:
            if self.dialog_instance:
                return self.dialog_instance.next(self)
        except ValueError:
            raise AttributeError(f"Link '{self.name}' not found")
        return None

    @property
    def previous(self) -> Stage | None:
        try:
            if self.dialog_instance:
                return self.dialog_instance.previous(self)
        except ValueError:
            raise AttributeError(f"Link '{self.name}' not found")
        return None

    def get_extra(self, key: str, default: Any = None) -> Any:
        return self.extra.get(key, default)

    def set_extra(self, key: str, value: Any) -> None:
        self.extra[key] = value

    def set_extras(self, extra: dict[str, Any]) -> None:
        for k, v in extra.items():
            self.extra[k] = v
