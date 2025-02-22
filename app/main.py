from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.domain.mixins import Base
from app.routes import auth_routes, user_routes, transaction_routes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="UsersTransactions API",
    description="UsersTransactions",
    version="2025.2.1",
    lifespan=lifespan,
)

app.include_router(auth_routes.router, prefix="/v1/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/v1/users", tags=["users"])
app.include_router(transaction_routes.router, prefix="/v1/transactions", tags=["transactions"])
