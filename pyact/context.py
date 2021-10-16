"""
Copyright (c) 2021 ghcollin
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import inspect

from typing import List, Dict, Tuple, Callable, Coroutine, Generator, Union, Any, Optional, TypeVar

def to_async(fn: Callable[..., None]) -> Callable[..., None]:
    if inspect.iscoroutinefunction(fn):
        return fn
    else:
        async def wrap(*args, **kw_args):
            fn(*args, **kw_args)
        return wrap

ValType = TypeVar("ValType")
ResultType = TypeVar("ResultType")

def push(co : Coroutine[None, Optional[ValType], ResultType], val : ValType) -> ResultType:
    try:
        co.send(None)
        while True:
            co.send(val)
    except StopIteration as e:
        return e.value

def get_set(d : Dict, x : str, val : ValType, set : Optional[ValType] = None) -> ValType:
    if x not in d:
        d[x] = val
    if set is not None:
        d[x] = set
    return d[x]


import contextlib

class Context:
    def __init__(self):
        self._notify = asyncio.Event()
        self._state = {}
        self.state = lambda x, v, s = None: get_set(self._state, x, v, s)

    @contextlib.contextmanager
    def descend(self, key : Optional[str]) -> Generator[None, None, None]:
        old_getter = self.state
        if key:
            self.state = lambda x, v, s = None: get_set(old_getter(key, {}), x, v, s)
        yield
        self.state = old_getter

    def event_callback(self, fn: Callable[..., None], values: List[str] = None) -> Dict:
        self._callbacks.append(to_async(fn))
        return {
            '__is_callback': True,
            'cbs': [{
                'key': len(self._callbacks)-1,
                'values': values if values else []
            }]
        }

    async def call_event(self, json: Dict) -> None:
        cb = self._callbacks[json['key']]
        await cb(*json['values'])
        #if len(json['values']) > 0:
        #    await cb(json['values'])
        #else:
        #    await cb()

    def render(self, comp: Callable[[], Coroutine[None, Optional['Context'], ResultType]], base_callbacks: List[Callable[..., None]] = []) -> ResultType:
        self._callbacks = base_callbacks.copy()
        return push(comp(), self)

    def notify(self, dont_notify : Any = None) -> None:
        if self is not dont_notify:
            self._notify.set()

    async def wait(self) -> None:
        await self._notify.wait()
        self._notify.clear()

Component = Coroutine[None, Optional[Context], Dict]

def indep_async(fn):
    async def wrap() -> ResultType:
        x = fn()
        return (await x) if inspect.iscoroutine(x) else x
    return wrap

class GlobalContext(Context):
    def __init__(self):
        super().__init__()
        self._listeners = set()

    def notify(self, dont_notify : Optional[Context] = None):
        for ctx in self._listeners:
            ctx.notify(dont_notify)

    def new_local_context(self) -> Context:
        ctx = Context()
        self._listeners.add(ctx)
        return ctx

    def remove_listener(self, ctx: Context) -> None:
        self._listeners.remove(ctx)

    def render(self, _, __ = []):
        raise Exception()

    def render_app(self, pyact_app) -> Tuple[Callable[[], 'Component'], List[Callable[..., None]]]:
        return super().render(indep_async(pyact_app)), self._callbacks

Child = Union[str, Component]
ChildList = Union[Child, List[Optional[Child]]]