from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, MessageServiceDep
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter(
    prefix="/chats/{chat_id}/messages",
    tags=["messages"],
)


@router.post(
    "",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    chat_id: UUID,
    data: MessageCreate,
    user: CurrentUser,
    service: MessageServiceDep,
):
    return await service.create(
        chat_id=chat_id,
        user=user,
        data=data,
    )


@router.get(
    "",
    response_model=list[MessageRead],
)
async def get_messages(
    chat_id: UUID,
    user: CurrentUser,
    service: MessageServiceDep,
):
    return await service.get_all(
        chat_id=chat_id,
        user=user,
    )
