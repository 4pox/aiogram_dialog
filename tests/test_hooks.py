from typing import List, Callable

import pytest

from aiogram_dialog.hooks import Hook, HookPriority, HookType, StageHooks


class TestStageHook:

    @pytest.fixture
    def stage_hooks(self) -> StageHooks:
        return StageHooks()

    @pytest.fixture
    def list_call_hooks(self) -> List[Callable]:
        def call1() -> str:
            return "Working Hook1"

        def call2() -> str:
            return "Working Hook2"

        def call3() -> str:
            return "Working Hook3"

        return [call1, call2, call3]

    @pytest.fixture
    def list_hooks(self, list_call_hooks: List[Callable]) -> list[Hook]:
        hook1 = Hook(
            "hook1", HookType.PRE_PROCESS, list_call_hooks[0], HookPriority.HIGHEST
        )
        hook2 = Hook(
            "hook2", HookType.PRE_PROCESS, list_call_hooks[1], HookPriority.LOW
        )
        hook3 = Hook(
            "hook3", HookType.PRE_PROCESS, list_call_hooks[2], HookPriority.HIGH
        )
        return [hook1, hook2, hook3]

    def test_add_hook(self, stage_hooks: StageHooks, list_hooks: list[Hook]) -> None:
        stage_hooks.add(list_hooks[0])
        stage_hooks.add(list_hooks[1])
        stage_hooks.add(list_hooks[2])

        assert len(stage_hooks.hooks[HookType.PRE_PROCESS]) == 3
        assert stage_hooks.hooks[HookType.PRE_PROCESS][0].priority == 10
        assert stage_hooks.hooks[HookType.PRE_PROCESS][-1].priority == -5

    def test_add_list_hooks(
        self, stage_hooks: StageHooks, list_hooks: List[Hook]
    ) -> None:
        stage_hooks.add(list_hooks)

        assert len(stage_hooks.hooks[HookType.PRE_PROCESS]) == 3
        assert stage_hooks.hooks[HookType.PRE_PROCESS][0].priority == 10
        assert stage_hooks.hooks[HookType.PRE_PROCESS][-1].priority == -5

    def test_create(
        self, stage_hooks: StageHooks, list_call_hooks: List[Callable]
    ) -> None:
        stage_hooks.create(
            "created_hook",
            HookType.PRE_PROCESS,
            list_call_hooks[0],
            HookPriority.HIGHEST,
        )

        assert len(stage_hooks.hooks[HookType.PRE_PROCESS]) > 0
        assert stage_hooks.hooks[HookType.PRE_PROCESS][-1].name == "created_hook"

    def test_get_by_type(self, stage_hooks: StageHooks, list_hooks: list[Hook]) -> None:
        stage_hooks.add(list_hooks)

        hook: List[Hook] = stage_hooks.get_all_by_type(HookType.PRE_PROCESS)

        assert len(hook) > 1
        assert hook[-1].priority == -5

    def test_get_by_name(self, stage_hooks: StageHooks, list_hooks: List[Hook]) -> None:
        stage_hooks.add(list_hooks)

        hook: Hook | None = stage_hooks.get_by_name("hook2")
        if hook:
            assert hook.name == "hook2"

    def test_get_all(self, stage_hooks: StageHooks, list_hooks: List[Hook]) -> None:
        stage_hooks.add(list_hooks)

        assert len(stage_hooks.get_all) == 3

        for i in stage_hooks.get_all:
            assert isinstance(i, Hook)

    def test_remove(self, stage_hooks: StageHooks, list_hooks: List[Hook]) -> None:
        stage_hooks.add(list_hooks)

        assert len(stage_hooks.hooks[HookType.PRE_PROCESS]) == 3

        stage_hooks.remove(list_hooks[1])

        assert len(stage_hooks.hooks[HookType.PRE_PROCESS]) == 2
        assert stage_hooks.hooks[HookType.PRE_PROCESS][-1].priority == 5
