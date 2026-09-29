from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import Chat
from app.models.user import User
from app.schemas.chat import ChatUpdate


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user: User,
    ) -> Chat:
        chat = Chat(
            user_id=user.id,
        )

        self.db.add(chat)

        await self.db.commit()
        await self.db.refresh(chat)

        return chat

    async def get_all(
        self,
        user: User,
    ) -> list[Chat]:
        stmt = (
            select(Chat).where(Chat.user_id == user.id).order_by(Chat.updated_at.desc())
        )

        result = await self.db.scalars(stmt)

        return list(result.all())

    async def get(
        self,
        chat_id: UUID,
        user: User,
    ) -> Chat:
        stmt = select(Chat).where(
            Chat.id == chat_id,
            Chat.user_id == user.id,
        )

        chat = await self.db.scalar(stmt)

        if chat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        return chat

    async def update(
        self,
        chat_id: UUID,
        user: User,
        data: ChatUpdate,
    ) -> Chat:
        chat = await self.get(
            chat_id=chat_id,
            user=user,
        )

        chat.title = data.title

        await self.db.commit()
        await self.db.refresh(chat)

        return chat

    async def delete(
        self,
        chat_id: UUID,
        user: User,
    ) -> None:
        chat = await self.get(
            chat_id=chat_id,
            user=user,
        )

        await self.db.delete(chat)
        await self.db.commit()
