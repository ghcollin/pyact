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

from .context import Context, Component, ChildList
from typing import Collection, ContextManager, Coroutine, TypeVar, Tuple, List, Callable, Generator, Optional, Dict, Union, Any, TypeVar, cast, Awaitable

from pyact import context

StateType = TypeVar("StateType")

import asyncio

class ExternalState:
    def __init__(self, val: StateType):
        self.get = val
        def set(x : StateType) -> None:
            self.get = x
        self.set = set

    def __await__(self) -> Generator[None, Context, Tuple[StateType, Callable[[StateType], None]]]:
        ctx = yield
        def set(x : StateType) -> None:
            self.get = x
            ctx.notify()
        self.set = set
        return self.get, set

@asyncio.coroutine
def _state(name : str, init : StateType) -> Generator[None, Context, Tuple[StateType, Callable[[StateType], None]]]:
    ctx = yield
    state = ctx.state
    def set(x : StateType) -> None:
        state(name, init, x)
        ctx.notify()
    return state(name, init), set

async def state(name : str, init_val : StateType) -> Tuple[StateType, Callable[[StateType], None]]:
    return await _state(name, init_val)
    
@asyncio.coroutine
def _callback(fn : Callable[..., None], values : Optional[List[str]]) -> Generator[None, Context, Dict]:
    ctx : Context = yield
    return ctx.event_callback(fn, values)

async def callback(fn : Callable[..., None], values : Optional[List[str]] = None) -> Dict:
    return await _callback(fn, values)

import inspect

@asyncio.coroutine
def descend(key : Optional[str]) -> Generator[None, Context, ContextManager[None]]:
    return (yield).descend(key)

async def scope(name : str) -> ContextManager[None]:
    return await descend(name)

async def await_eval(o : Any) -> Any:
    return cast(Any, {**(await o), '__is_object': True}) if inspect.iscoroutine(o) else \
        (await recurse_await(o) if isinstance(o, (dict, list)) else o)

CollectionT = TypeVar('CollectionT', bound=Union[Dict, List])

async def recurse_await(c: CollectionT) -> CollectionT:
    if isinstance(c, list):
        for i, v in enumerate(c):
            c[i] = await await_eval(v)
    elif isinstance(c, dict):
        for k, v in c.items():
            c[k] = await await_eval(v)
    else:
        raise TypeError()
    return c

async def basic_element(el: str, id: Optional[str], key: Optional[str], props: Optional[Dict], children: Optional[ChildList], **kw_args) -> Dict:
    with await descend(key):
        props = {**kw_args, **(props if props else ({'key':key} if key else {}))}
        props = await recurse_await(props)
        Item = Union[str, Dict]
        items : Optional[Union[Item, List[Item]]]
        if isinstance(children, list):
            contents : List[Optional[Item]] = children # type: ignore
            for i, v in enumerate(children):
                contents[i] = (await cast(Awaitable[Dict], v)) if inspect.iscoroutine(v) else cast(Optional[str], v)
            items = [ e for e in contents if e ]
        else:
            items = (await cast(Awaitable[Dict], children)) if inspect.iscoroutine(children) else cast(Optional[str], children)
        return {
            'el': "{}#{}".format(el, id) if id else el,
            'props' : props,
            'children': items
        }

Callback = Coroutine[None, Optional[Context], Dict]

async def combine_cb_dicts(a: Callback, b: Callback) -> Dict:
    cba, cbb = await a, await b
    cba['cbs'].append(cbb['cbs'][0])
    return cba

def combine_callbacks(props: Optional[Dict], name: str, cb: Callback) -> Dict:
    if props is None:
        return {name: cb}
    else:
        props = props.copy()
        if name in props:
            props[name] = combine_cb_dicts(props[name], cb)
        else:
            props[name] = cb
        return props

def javascript_fn(name: str, *args) -> Dict:
    return  {
        '__is_fn': True,
        'fn': name,
        'args': args
    }

def create_namespace_element(namespace : str):
    def create_element(name : str):
        el = namespace + name
        def comp(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, children: Optional[ChildList] = None, **kw_args) -> Component:
            return basic_element(el, id, key, props, children, **kw_args)
        return comp
    def create_void_element(name : str):
        el = namespace + name
        def comp(id: Optional[str] = None, key: Optional[str] = None, props: Optional[Dict] = None, **kw_args) -> Component:
            return basic_element(el, id, key, props, None, **kw_args)
        return comp
    return create_element, create_void_element
