import asyncio
import inspect

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

    def event_callback(self, fn, values=None):
        self._callbacks.append(to_async(fn))
        return {
            '__is_callback': True,
            'cbs': [{
                'key': len(self._callbacks)-1,
                'values': values if values else []
            }]
        }

    async def call_event(self, json):
        cb = self._callbacks[json['key']]
        if len(json['values']) > 0:
            await cb(json['values'])
        else:
            await cb()

    def next_key(self):
        self._key += 1
        return str(self._key)

    def render(self, app):
        self._callbacks = []
        self._key = 0
        return app(self)

    def notify(self):
        self._notify.set()

    async def wait(self):
        await self._notify.wait()
        self._notify.clear()