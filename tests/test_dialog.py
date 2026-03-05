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

    def test_init(self, router: Router) -> None:
        dialog = Dialog(router=router)

        assert dialog.router == router
        assert dialog.stages == {}
        assert dialog.stage_orders == []

    def test_add_stage(self, dialog: Dialog, sample_stage: List[Stage]) -> None:
        stage: Stage = sample_stage[0]

        dialog.add_stage(stage)

        added_stage: Stage | None = dialog.get_stage_by_name("a")
        if added_stage is not None:
            assert isinstance(added_stage.dialog_instance, Dialog)

        assert "a" in dialog.stages

    def test_get_stage(self, dialog: Dialog, sample_stage: List[Stage]) -> None:
        dialog.add_stages(sample_stage)

        assert dialog.get_stage_by_name("b") == sample_stage[1]
        assert dialog.get_stage_by_name(sample_stage[1]) == sample_stage[1]
        assert dialog.next(sample_stage[1]) == sample_stage[-1]
        assert dialog.previous(sample_stage[1]) == sample_stage[0]
        assert dialog.get_first_stage == sample_stage[0]
        assert dialog.get_last_stage == sample_stage[-1]

    def test_get_stage_index(self, dialog: Dialog, sample_stage: List[Stage]) -> None:
        dialog.add_stages(sample_stage)

        assert dialog.get_stage_index(sample_stage[1]) == 1
        assert dialog.get_next_stage_index(sample_stage[1]) == 2
        assert dialog.get_previous_stage_index(sample_stage[1]) == 0

    def test_remove_stage_index(
        self, dialog: Dialog, sample_stage: List[Stage]
    ) -> None:
        dialog.add_stages(sample_stage)

        dialog.remove(sample_stage[1])

        assert len(dialog) == 2
        assert "b" not in dialog.stages
