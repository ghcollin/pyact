
from .context import Context
from typing import TypeVar, Tuple, Callable, Optional, Dict, Any

StateType = TypeVar("StateType")

class ComponentState:
    def __init__(self):
        self._state = {}
        self._listeners = set()

    def _notify(self, dont_notify: Optional[Context]) -> None:
        for ctx in self._listeners:
            if ctx is not dont_notify:
                ctx.notify()

    def create(self, key: str, init: StateType) -> Tuple[StateType, Callable[[StateType, Optional[Context]], None]]:
        if key not in self._state:
            self._state[key] = init
        def setState(val: StateType, dont_notify: Optional[Context] = None) -> None:
            self._state[key] = val
            self._notify(dont_notify)

        return self._state[key], setState

    def add_listener(self, ctx: Context) -> None:
        self._listeners.add(ctx)

from .types import PyactApp

# Not yet supported by mypy
# from typing_extensions import Protocol

# class StateComponent(Protocol):
#     def __call__(self, __state: ComponentState, __ctx: Context, *__args: Any, **__kw_args: Any) -> PyactApp:
#         pass

# class Component(Protocol):
#     def __call__(self, *__args: Any, **__kw_args: Any) -> PyactApp:
#         pass

def state(comp): 
    def wrap(*args, **kw_args) -> PyactApp:
        state = ComponentState()
        return lambda ctx: comp(state, ctx, *args, **kw_args)(ctx)
    return wrap

def combine_callbacks(props: Optional[Dict], name: str, cb: Dict) -> Dict:
    if props is None:
        return {name: cb}
    else:
        props = props.copy()
        if name in props:
            props[name]['cbs'].append(cb['cbs'][0])
        else:
            props[name] = cb
        return props

