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

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
from typing import Callable, Any
import asyncio

from .context import Context
from .types import PyactApp

def create_app(pyact_app: Callable[[], PyactApp], index_html: str) -> Starlette:
    app = Starlette(debug=True)

    @app.websocket_route("/ws")
    class WebSocketLoop(WebSocketEndpoint):
        encoding = 'json'

        async def on_connect(self, websocket: WebSocket) -> None:
            await websocket.accept(subprotocol='json')
            self.pyact_app = pyact_app()
            self.ctx = Context()
            await websocket.send_json(self.ctx.render(self.pyact_app))

            self.notify_task = asyncio.create_task(self.notify_loop(websocket))

        async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
            print(close_code)
            self.notify_task.cancel()

        async def on_receive(self, websocket: WebSocket, data: Any) -> None:
            await self.ctx.call_event(data)

        async def notify_loop(self, websocket: WebSocket) -> None:
            while True:
                await self.ctx.wait()
                await websocket.send_json(self.ctx.render(self.pyact_app))

    @app.route("/")
    class Homepage(HTTPEndpoint):
        async def get(self, _):
            return HTMLResponse(index_html)

    return app