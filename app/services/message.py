from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate
from app.services.ai import OpenAIService
from app.services.chat import ChatService


class MessageService:
    def __init__(
        self,
        db: AsyncSession,
        chat_service: ChatService,
        openai_service: OpenAIService,
    ):
        self.db = db
        self.chat_service = chat_service
        self.openai_service = openai_service

    async def create(
        self,
        chat_id: UUID,
        user: User,
        data: MessageCreate,
    ) -> Message:
        # 1. 해당 채팅이 현재 사용자의 것인지 확인
        await self.chat_service.get(
            chat_id=chat_id,
            user=user,
        )

        # 2. 기존 대화 조회
        previous_messages = await self._get_messages(
            chat_id=chat_id,
        )

        # 3. 새 사용자 메시지 생성
        user_message = Message(
            chat_id=chat_id,
            role="user",
            content=data.content,
        )

        self.db.add(user_message)

        # 아직 commit하지 않음
        await self.db.flush()

        # 4. OpenAI에 넘길 context 생성
        context = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in previous_messages
        ]

        context.append(
            {
                "role": "user",
                "content": data.content,
            }
        )

        try:
            # 5. OpenAI 호출
            assistant_content = await self.openai_service.generate(
                messages=context,
            )

            # 6. assistant 메시지 생성
            assistant_message = Message(
                chat_id=chat_id,
                role="assistant",
                content=assistant_content,
            )

            self.db.add(assistant_message)

            # user + assistant 한 번에 저장
            await self.db.commit()
            await self.db.refresh(assistant_message)

            return assistant_message

        except Exception:
            await self.db.rollback()
            raise

    async def get_all(
        self,
        chat_id: UUID,
        user: User,
    ) -> list[Message]:
        await self.chat_service.get(
            chat_id=chat_id,
            user=user,
        )

        return await self._get_messages(
            chat_id=chat_id,
        )

    async def _get_messages(
        self,
        chat_id: UUID,
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
        )

        result = await self.db.scalars(stmt)

        return list(result.all())
