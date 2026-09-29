from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.message import router as message_router
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, fastapi_users

router = APIRouter()

# Auth
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# Users
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Chat
router.include_router(chat_router)

# Message
router.include_router(message_router)
