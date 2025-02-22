from fastapi import HTTPException, status

from app.core import security
from app.domain.enums import UserRole


async def authenticate_token(token: str, _) -> dict:
    payload = security.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("id")
    role_str = payload.get("role")
    if not user_id or not role_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        role = UserRole(role_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid role in token")

    return {"id": user_id, "role": role}
