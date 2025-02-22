from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.database import get_db
from app.dependencies import get_user_repository, get_staff_repository
from app.domain.enums import UserRole

router = APIRouter()


@router.post("/users")
async def user_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
        user_repo=Depends(get_user_repository)
):
    user = await user_repo.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    token = security.create_access_token({"id": user.id, "role": UserRole.user.value})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/staff")
async def staff_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
        staff_repo=Depends(get_staff_repository)
):
    staff = await staff_repo.get_staff_by_login(db, form_data.username)
    if not staff:
        raise HTTPException(status_code=401, detail="Invalid staff login")

    token = security.create_access_token({"id": staff.id, "role": UserRole.staff.value})

    return {"access_token": token, "token_type": "bearer"}
