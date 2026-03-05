import pytest

from typing import List

from aiogram import Router
from aiogram.filters import Command

from aiogram_dialog.dialog import Dialog
from aiogram_dialog.dialog import Stage
from aiogram_dialog.handler import HandlerConfig, HandlerType


class TestDialog:

    @pytest.fixture
    def router(self) -> Router:
        return Router(name="dialog_router")

    @pytest.fixture
    def dialog(self, router: Router) -> Dialog:
        return Dialog(router)

    @pytest.fixture
    def sample_stage(self) -> List[Stage]:
        a = Stage(
            id=1,
            name="a",
            state=None,
            handler=HandlerConfig(HandlerType.MESSAGE, Command("a", prefix="/")),
        )
        b = Stage(
            id=1,
            name="b",
            state=None,
            handler=HandlerConfig(HandlerType.MESSAGE, Command("b", prefix="/")),
        )
        c = Stage(
            id=1,
            name="c",
            state=None,
            handler=HandlerConfig(HandlerType.MESSAGE, Command("c", prefix="/")),
        )
        return [a, b, c]

    @pytest.fixture
    def sample_extra(self) -> dict[str, int]:
        return {"a": 1, "b": 2, "c": 3}

    def test_next_stage(self, dialog: Dialog, sample_stage: List[Stage]) -> None:
        dialog.add_stages(sample_stage)
        current_stage: Stage = sample_stage[1]
        active_stage_in_dialog: Stage | None = dialog.get_stage_by_name(current_stage)

        if active_stage_in_dialog:
            next_stage: Stage | None = active_stage_in_dialog.next
            if next_stage:
                assert next_stage.name == "c"

    def test_previous_stage(self, dialog: Dialog, sample_stage: List[Stage]) -> None:
        dialog.add_stages(sample_stage)

        current_stage: Stage = sample_stage[1]
        active_stage_in_dialog: Stage | None = dialog.get_stage_by_name(current_stage)

        if active_stage_in_dialog:
            previous_stage: Stage | None = active_stage_in_dialog.previous
            if previous_stage:
                assert previous_stage.name == "a"

    def test_extra(
        self, dialog: Dialog, sample_stage: List[Stage], sample_extra: dict[str, int]
    ) -> None:
        dialog.add_stages(sample_stage)

        current_stage: Stage = sample_stage[1]
        active_stage_in_dialog: Stage | None = dialog.get_stage_by_name(current_stage)

        if active_stage_in_dialog:
            active_stage_in_dialog.set_extras(sample_extra)
            active_stage_in_dialog.set_extra("d", 4)

            assert len(active_stage_in_dialog.extra) == 4
            assert active_stage_in_dialog.extra["d"] == 4
