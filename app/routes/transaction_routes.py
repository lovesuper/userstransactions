from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_transaction_service, get_auth_service, get_user_repository
from app.domain.enums import UserRole
from app.schemas.jsonapi import TransactionCreateRequest
from app.utils.jsonapi import jsonapi_response

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("", response_model=dict)
async def create_transaction(
        transaction: TransactionCreateRequest,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        transaction_service=Depends(get_transaction_service),
        auth_service=Depends(get_auth_service),
        user_repo=Depends(get_user_repository),

):
    auth = await auth_service.authenticate_token(token, db)
    if auth["role"] != UserRole.staff:
        raise HTTPException(status_code=403, detail="Only staff can create transactions")

    user = await user_repo.get_user_by_id(db, transaction.data.attributes.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.verified is None:
        raise HTTPException(status_code=404, detail="User not verified")

    try:
        new_transaction = await transaction_service.register_transaction(
            db, transaction.data.attributes.model_dump(), auth["id"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return jsonapi_response(new_transaction)
