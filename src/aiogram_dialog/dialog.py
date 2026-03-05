from __future__ import annotations
from typing import Dict, List

from aiogram import Router

from .stage import Stage


class Dialog:

    _stages: Dict[str, Stage]
    _stage_orders: List[str]
    _router: Router

    def __init__(self, router: Router) -> None:
        self._router = router
        self._stage_orders = []
        self._stages = {}

    def __len__(self) -> int:
        return len(self.stages)

    def set_router(self, router: Router) -> None:
        self._router = router

    @property
    def router(self) -> Router:
        return self._router

    @property
    def stages(self) -> Dict[str, Stage]:
        return self._stages

    @property
    def stage_orders(self) -> List[str]:
        return self._stage_orders

    def add_stage(self, stage: Stage) -> None:
        if isinstance(stage, Stage):
            if stage.name in self._stages:
                raise ValueError(f"Stage {stage.name} already exists")

            stage._set_dialog_instance(self)
            stage._set_router(self.router)

            self._stages[stage.name] = stage
            self._stage_orders.append(stage.name)

    def add_stages(self, stages: list[Stage]) -> None:
        for stage in stages:
            self.add_stage(stage)

    def get_stage_index(self, stage: Stage) -> int:
        return self._stage_orders.index(stage.name)

    def get_next_stage_index(self, stage: Stage) -> int:
        return self._stage_orders.index(stage.name) + 1

    def get_previous_stage_index(self, stage: Stage) -> int:
        return self._stage_orders.index(stage.name) - 1

    @property
    def get_last_stage(self) -> Stage | None:
        return self.get_stage_by_name(self._stage_orders[-1])

    @property
    def get_first_stage(self) -> Stage | None:
        return self.get_stage_by_name(self._stage_orders[0])

    def get_stage_by_name(self, stage: Stage | str) -> Stage | None:
        if isinstance(stage, Stage):
            return self._stages.get(stage.name)
        elif isinstance(stage, str):
            return self._stages.get(stage)
        else:
            return None

    def next(self, stage: Stage) -> Stage | None:
        return self.get_stage_by_name(
            self._stage_orders[self.get_next_stage_index(stage)]
        )

    def previous(self, stage: Stage) -> Stage | None:
        return self.get_stage_by_name(
            self._stage_orders[self.get_previous_stage_index(stage)]
        )

    def remove(self, stage: Stage | str) -> None:
        if isinstance(stage, Stage):
            if stage.name in self.stages:
                del self._stages[stage.name]
                self._stage_orders.remove(stage.name)
        if isinstance(stage, str):
            if stage in self.stages:
                del self._stages[stage]
                self._stage_orders.remove(stage)
