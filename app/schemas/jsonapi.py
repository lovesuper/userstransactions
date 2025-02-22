from pydantic import BaseModel, model_validator

from app.schemas.schemas import UserCreate, TransactionCreate


class JSONAPIData(BaseModel):
    type: str
    attributes: dict

    @classmethod
    @model_validator(mode="before")
    def check_keys(cls, values):
        if "type" not in values or "attributes" not in values:
            raise ValueError("JSONAPI object must contain 'type' and 'attributes'")

        return values


class JSONAPIRequest(BaseModel):
    data: JSONAPIData

    @classmethod
    @model_validator(mode="after")
    def check_data(cls, values):
        if values.data is None:
            raise ValueError("Missing 'data' key")

        return values


class UserCreateData(BaseModel):
    type: str
    attributes: UserCreate

    @classmethod
    @model_validator(mode="before")
    def check_type(cls, values: dict) -> dict:
        if values.get("type") != "users":
            raise ValueError("Invalid type, must be 'users'")

        return values


class TransactionCreateData(BaseModel):
    type: str
    attributes: TransactionCreate

    @classmethod
    @model_validator(mode="before")
    def check_type(cls, values: dict) -> dict:
        if values.get("type") != "transactions":
            raise ValueError("Invalid type, must be 'users'")

        return values


class UserCreateRequest(BaseModel):
    data: UserCreateData


class TransactionCreateRequest(BaseModel):
    data: TransactionCreateData
