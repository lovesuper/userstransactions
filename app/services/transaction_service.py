from app.domain.transaction import Transaction, OperationType
from app.repositories import transaction_repository


async def register_transaction(db, transaction_data: dict, staff_id: str) -> Transaction:
    if not isinstance(transaction_data["operation_type"], OperationType):
        transaction_data["operation_type"] = OperationType(transaction_data["operation_type"])

    if transaction_data["operation_type"] == OperationType.writeoff:
        current_balance = await transaction_repository.get_user_balance(db, transaction_data["user_id"])
        if float(transaction_data["amount"]) > current_balance:
            raise Exception("Insufficient funds: Cannot withdraw more than current balance")

    transaction = Transaction(**transaction_data)
    transaction.staff_id = staff_id

    return await transaction_repository.create_transaction(db, transaction)
