from typing_extensions import Self
from Remilia.fancy import toInstanceWithArgs,hasInstanceWithArgs
from .config import getElse
from aiohttp import ClientSession
import asyncio




@toInstanceWithArgs(getElse("mdv_host","127.0.0.1"),getElse("mdv_port",9098))
@hasInstanceWithArgs(getElse("mdv_host","127.0.0.1"),getElse("mdv_port",9098))
class MarkDovenClient:
    instance:Self
    def __init__(self, host: str, port: int) -> None:
        self.address = "http://%s:%s" % (host, port)
    async def renderText(
        self, text: str, isdark: bool = True, sleepsec: float = 1
    ) -> bytes:
        async with ClientSession() as session:
            async with session.post(
                self.address + "/api/generate", json={"text": str(text), "isdark": isdark}
            ):
                await asyncio.sleep(sleepsec)
                async with session.get(self.address + "/api/screenshot") as resp:
                    return await resp.content.read()
