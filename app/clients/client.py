from typing import Protocol

from openai import AsyncOpenAI


class AIClient(Protocol):
    async def generate(self, *, model: str, prompt: str) -> str:
        ...


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def generate(self, *, prompt: str) -> str:
        response = await self._client.responses.create(
            model=self._model,
            input=prompt,
        )

        return response.output_text