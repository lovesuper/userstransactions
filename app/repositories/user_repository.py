from typing import List, Optional

from sqlalchemy import false
from sqlalchemy.future import select

from app.domain.user import User


async def create_user(db, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_id(db, user_id: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.id == user_id, User.is_deleted is false()))

    return result.scalar_one_or_none()


async def get_user_by_username(db, username: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.username == username, User.is_deleted is false()))

    return result.scalar_one_or_none()


async def get_users(db, username_filter: Optional[str] = None, verified: Optional[bool] = None) -> List[User]:
    query = select(User).filter(User.is_deleted is false())
    if username_filter:
        query = query.filter(User.username.ilike(f"%{username_filter}%"))

    if verified is not None:
        if verified:
            query = query.filter(User.verified.isnot(None))
        else:
            query = query.filter(User.verified.is_(None))

    result = await db.execute(query)

    return result.scalars().all()


async def update_user(db, user: User, updates: dict) -> User:
    for key, value in updates.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(db, user: User):
    user.is_deleted = True
    await db.commit()

    return user
