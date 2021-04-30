from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
import typing
import asyncio

from .context import Context
from .types import PyactApp

def create_app(pyact_app: PyactApp, index_html: str) -> Starlette:
    app = Starlette(debug=True)

    @app.websocket_route("/ws")
    class WebSocketLoop(WebSocketEndpoint):
        encoding = 'json'

        async def on_connect(self, websocket: WebSocket) -> None:
            await websocket.accept(subprotocol='json')
            self.ctx = Context()
            await websocket.send_json(self.ctx.render(pyact_app))

            self.notify_task = asyncio.create_task(self.notify_loop(websocket))

        async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
            print(close_code)
            self.notify_task.cancel()

        async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
            await self.ctx.call_event(data)

        async def notify_loop(self, websocket: WebSocket) -> None:
            while True:
                await self.ctx.wait()
                await websocket.send_json(self.ctx.render(pyact_app))

    @app.route("/")
    class Homepage(HTTPEndpoint):
        async def get(self, _):
            return HTMLResponse(index_html)

    return app