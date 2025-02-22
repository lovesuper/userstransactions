from datetime import datetime, timezone

from fastapi import HTTPException
from starlette import status

from app.domain.user import User
from app.repositories import user_repository
from app.schemas.schemas import UserCreate


async def register_user(db, user_data: UserCreate) -> User:
    existing_user = await user_repository.get_user_by_username(db, user_data.username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{user_data.username}' already exists."
        )

    user = User(**user_data.model_dump())

    return await user_repository.create_user(db, user)


async def update_user(db, user: User, updates: dict) -> User:
    forbidden_keys = {'username', 'is_deleted', 'verified', 'created', 'modified'}
    filtered_updates = dict(filter(lambda item: item[0] not in forbidden_keys, updates.items()))
    new_updates = {**filtered_updates, "modified":  datetime.now(timezone.utc)}

    return await user_repository.update_user(db, user, new_updates)


async def get_users(db, username_filter: str = None, verified: bool = None):
    return await user_repository.get_users(db, username_filter, verified)
