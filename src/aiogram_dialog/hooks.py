from __future__ import annotations

import enum
from typing import Callable, List
from dataclasses import dataclass

from .utils import is_list_of


class HookType(enum.Enum):
    PRE_PROCESS = "pre_process"
    POST_PROCESS = "post_process"
    ERROR = "error"
    VALIDATION = "validation"


class HookPriority(enum.IntEnum):
    HIGHEST = 10
    HIGH = 5
    NORMAL = 0
    LOW = -5
    LOWEST = -10


@dataclass
class Hook:
    name: str
    type: HookType
    call: Callable
    priority: HookPriority = HookPriority.NORMAL

    def __post_init__(self) -> None:
        if not callable(self.call):
            raise ValueError(f"Hook call must be callable, got {type(self.call)}")


class StageHooks:

    def __init__(self) -> None:
        self.hooks: dict[HookType, List[Hook]] = {
            hook_type: [] for hook_type in HookType
        }

    def add(self, hook: Hook | List[Hook]) -> None:
        if isinstance(hook, list):
            if not is_list_of(hook, Hook):
                raise TypeError("All elements in the list must be of type Hook")
            hooks_to_add: List[Hook] = hook
        elif isinstance(hook, Hook):
            hooks_to_add = [hook]
        else:
            raise TypeError(f"Expected Hook or List[Hook], got {type(hook)}")

        for h in hooks_to_add:
            hook_type: HookType = h.type
            if hook_type not in self.hooks:
                self.hooks[hook_type] = []
            self.hooks[hook_type].append(h)

        for hook_type in {h.type for h in hooks_to_add}:
            self.hooks[hook_type].sort(key=lambda h: h.priority.value, reverse=True)

    def create(
        self,
        name: str,
        hook_type: HookType,
        callback: Callable,
        priority: HookPriority = HookPriority.NORMAL,
    ) -> Hook:
        hook = Hook(name=name, type=hook_type, call=callback, priority=priority)
        self.add(hook)
        return hook

    def remove(self, hook: Hook) -> bool:
        hook_list: List[Hook] = self.hooks[hook.type]
        if hook in hook_list:
            hook_list.remove(hook)
            return True
        return False

    def get_by_name(self, name: str) -> Hook | None:
        if not self.hooks:
            return None
        for hook_list in self.hooks.values():
            for hook in hook_list:
                if hook.name == name:
                    return hook
        return None

    def get_all_by_type(self, hook_type: HookType) -> List[Hook]:
        return self.hooks[hook_type].copy()

    @property
    def get_all(self) -> List[Hook]:
        all_hooks: list[Hook] = []
        for hook_list in self.hooks.values():
            all_hooks.extend(hook_list)
        return all_hooks

    pass
