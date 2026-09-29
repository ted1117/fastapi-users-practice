from openai import AsyncOpenAI

from app.core.config import Settings


class OpenAIService:
    def __init__(self, settings: Settings):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )
        self.model = settings.openai_model

    async def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        response = await self.client.responses.create(
            model=self.model,
            instructions="사용자의 질문에 정확하고 간결하게 답변하세요.",
            input=messages,
            store=False,
        )

        return response.output_text
