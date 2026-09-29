from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import ChatServiceDep, CurrentUser
from app.schemas.chat import ChatRead, ChatUpdate

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.post(
    "",
    response_model=ChatRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat(
    user: CurrentUser,
    service: ChatServiceDep,
):
    return await service.create(user=user)


@router.get(
    "",
    response_model=list[ChatRead],
)
async def get_chats(
    user: CurrentUser,
    service: ChatServiceDep,
):
    return await service.get_all(user=user)


@router.get(
    "/{chat_id}",
    response_model=ChatRead,
)
async def get_chat(
    chat_id: UUID,
    user: CurrentUser,
    service: ChatServiceDep,
):
    return await service.get(
        chat_id=chat_id,
        user=user,
    )


@router.patch(
    "/{chat_id}",
    response_model=ChatRead,
)
async def update_chat(
    chat_id: UUID,
    data: ChatUpdate,
    user: CurrentUser,
    service: ChatServiceDep,
):
    return await service.update(
        chat_id=chat_id,
        user=user,
        data=data,
    )


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat(
    chat_id: UUID,
    user: CurrentUser,
    service: ChatServiceDep,
):
    await service.delete(
        chat_id=chat_id,
        user=user,
    )
