from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_user_repository, get_user_service, get_auth_service, get_transaction_repository
from app.domain.enums import UserRole
from app.schemas.jsonapi import UserCreateRequest
from app.utils.jsonapi import jsonapi_response

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("", response_model=dict)
async def create_user(
        payload: UserCreateRequest,
        db: AsyncSession = Depends(get_db),
        user_service=Depends(get_user_service)
):
    new_user = await user_service.register_user(db, payload.data.attributes)

    return jsonapi_response(new_user)


@router.get("", response_model=dict)
async def list_users(
        username: Optional[str] = None,
        verified: Optional[bool] = None,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        user_service=Depends(get_user_service),
        auth_service=Depends(get_auth_service)
):
    auth = await auth_service.authenticate_token(token, db)
    if auth["role"] != UserRole.staff:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    users = await user_service.get_users(db, username_filter=username, verified=verified)

    return jsonapi_response(users)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
        user_id: str,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        user_repo=Depends(get_user_repository),
        auth_service=Depends(get_auth_service)
):
    auth = await auth_service.authenticate_token(token, db)
    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if auth["role"] != UserRole.staff:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    deleted_user = await user_repo.delete_user(db, user)

    return jsonapi_response(deleted_user)


@router.patch("/{user_id}", response_model=dict)
async def update_user(
        user_id: str,
        updates: dict,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        user_repo=Depends(get_user_repository),
        user_service=Depends(get_user_service),
        auth_service=Depends(get_auth_service)
):
    auth = await auth_service.authenticate_token(token, db)
    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if auth["role"] != UserRole.staff and auth["id"] != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated_user = await user_service.update_user(db, user, updates["data"]["attributes"])

    return jsonapi_response(updated_user)


@router.post("/{user_id}/verify", response_model=dict)
async def verify_user(
        user_id: str,
        verified: bool,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        user_repo=Depends(get_user_repository),
        auth_service=Depends(get_auth_service)
):
    auth = await auth_service.authenticate_token(token, db)
    if auth["role"] != UserRole.staff:
        raise HTTPException(status_code=403, detail="Only staff can change verification status")

    user = await user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {"verified": datetime.now()} if verified else {"verified": None}
    update_data['modified'] = datetime.now()
    updated_user = await user_repo.update_user(db, user, update_data)

    return jsonapi_response(updated_user)


@router.get("/{user_id}/transactions", response_model=dict)
async def user_transactions(
        user_id: str,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        auth_service=Depends(get_auth_service),
        transaction_repo=Depends(get_transaction_repository)
):
    auth = await auth_service.authenticate_token(token, db)
    if auth["role"] != UserRole.staff and auth["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    transactions = await transaction_repo.get_transactions_by_user(db, user_id)

    return jsonapi_response(transactions)


@router.get("/{user_id}/balance", response_model=dict)
async def user_balance(
        user_id: str,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        auth_service=Depends(get_auth_service),
        transaction_repo=Depends(get_transaction_repository)
):
    auth = await auth_service.authenticate_token(token, db)
    if auth["role"] != UserRole.staff and auth["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    balance = await transaction_repo.get_user_balance(db, user_id)

    return {"data": {"balance": balance}}
