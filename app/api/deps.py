from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db import get_db
from app.models.user import User
from app.services.ai import OpenAIService
from app.services.chat import ChatService
from app.services.message import MessageService
from app.users import current_active_user

DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(current_active_user),
]

SettingsDep = Annotated[
    Settings,
    Depends(get_settings),
]


def get_chat_service(
    db: DBSession,
) -> ChatService:
    return ChatService(db)


ChatServiceDep = Annotated[
    ChatService,
    Depends(get_chat_service),
]


def get_openai_service(
    settings: SettingsDep,
) -> OpenAIService:
    return OpenAIService(settings)


OpenAIServiceDep = Annotated[
    OpenAIService,
    Depends(get_openai_service),
]


def get_message_service(
    db: DBSession,
    chat_service: ChatServiceDep,
    openai_service: OpenAIServiceDep,
) -> MessageService:
    return MessageService(
        db=db,
        chat_service=chat_service,
        openai_service=openai_service,
    )


MessageServiceDep = Annotated[
    MessageService,
    Depends(get_message_service),
]
