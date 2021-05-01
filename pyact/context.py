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

from typing import List, Dict, Callable

JSON = Dict
PyactApp = Callable[['Context'], JSON]

def to_async(fn):
    if inspect.iscoroutinefunction(fn):
        return fn
    else:
        async def wrap(*args, **kw_args):
            fn(*args, **kw_args)
        return wrap

class Context:
    def __init__(self):
        self._notify = asyncio.Event()

    def event_callback(self, fn, values: List[str] = None) -> None:
        self._callbacks.append(to_async(fn))
        return {
            '__is_callback': True,
            'cbs': [{
                'key': len(self._callbacks)-1,
                'values': values if values else []
            }]
        }

    async def call_event(self, json: JSON) -> None:
        cb = self._callbacks[json['key']]
        if len(json['values']) > 0:
            await cb(json['values'])
        else:
            await cb()

    def next_key(self) -> str:
        self._key += 1
        return str(self._key)

    def render(self, pyact_app: PyactApp) -> JSON:
        self._callbacks = []
        self._key = 0
        return pyact_app(self)

    def notify(self) -> None:
        self._notify.set()

    async def wait(self) -> None:
        await self._notify.wait()
        self._notify.clear()