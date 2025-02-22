from typing import List

from sqlalchemy import case, func
from sqlalchemy.future import select

from app.domain.transaction import Transaction, OperationType


async def create_transaction(db, transaction: Transaction) -> Transaction:
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)

    return transaction


async def get_transactions_by_user(db, user_id: str) -> List[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id))

    return result.scalars().all()


async def get_user_balance(db, user_id: str) -> float:
    query = select(func.coalesce(func.sum(
        case(
            (Transaction.operation_type == OperationType.accrual, Transaction.amount),
            else_=-Transaction.amount
        )), 0)).filter(Transaction.user_id == user_id)

    result = await db.execute(query)
    balance = result.scalar_one()

    return float(balance)
