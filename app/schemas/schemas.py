import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserAttributes(BaseModel):
    city: str
    country: str
    created: Optional[datetime] = None
    email: EmailStr
    first_name: str
    is_deleted: bool = False
    last_name: str
    modified: Optional[datetime] = None
    username: str
    verified: Optional[datetime] = None


class UserCreate(BaseModel):
    city: str
    country: str
    email: EmailStr
    first_name: str
    last_name: str
    username: str


class TransactionOperationType(str, enum.Enum):
    accrual = "accrual"
    writeoff = "writeoff"


class TransactionAttributes(BaseModel):
    amount: float
    created: Optional[datetime] = None
    operation_type: TransactionOperationType
    staff_id: str
    user_id: str


class TransactionCreate(BaseModel):
    amount: float
    operation_type: TransactionOperationType
    user_id: str


class JSONAPIResponse(BaseModel):
    data: object
