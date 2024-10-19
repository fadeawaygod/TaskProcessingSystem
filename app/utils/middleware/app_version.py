from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.utils.logging.logger import get_logger

logger = get_logger()


class AppVersionMiddleware:
    """AppVersionMiddleware return app version in the response header."""

    def __init__(self, app: ASGIApp, app_version: str = "") -> None:
        self.app = app
        self.app_version = app_version

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            send_function = self._get_wrapped_send(send)
        else:
            send_function = send

        await self.app(scope, receive, send_function)

    def _get_wrapped_send(
        self,
        send: Send,
    ) -> Send:
        async def wrapped_send(message: Message):
            if message["type"] == "http.response.start":
                message["headers"].append((b"X-App-Version", self.app_version.encode()))
            await send(message)

        return wrapped_send
