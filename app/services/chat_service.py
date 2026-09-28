from app.clients.client import AIClient


class ChatService:
    def __init__(self, client: AIClient):
        self._client = client

    async def send_message(self, message: str) -> str:
        return await self._client.generate(prompt=message)