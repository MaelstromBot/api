from asyncio import wait_for, sleep

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        """A manager for incoming websocket connections."""

        self.connection: WebSocket = None

    async def connect(self, ws: WebSocket):
        if self.connection:
            try:
                await self.connection.close(4002)
            except:
                print("Error while closing existing WS to accommodate new connection.")
            finally:
                self.connection = None

        self.connection = ws

    async def close(self, code: int = 1000):
        try:
            await self.connection.close(code=code)
        except:
            print("Error while closing WS connection.")

    async def expect(self, message: dict, timeout: int = 3) -> dict:
        await self.connection.send_json({
            "op": "expect",
            "d": message
        })

        return await wait_for(self.connection.receive_json(), timeout=timeout)

    async def get_guild_permission(self, guild: int, member: int, permission: str) -> bool:
        try:
            result = await self.expect({
                "type": "guild_member_permissions",
                "params": {
                    "guild": guild,
                    "member": member,
                    "permission": permission
                }
            })

            return result["value"]
        except:
            return False  # Fail secure

    async def heartbeat(self):
        while True:
            await sleep(5)
            await self.connection.send_json({"op": "heartbeat"})
