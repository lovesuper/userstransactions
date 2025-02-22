from app.repositories import user_repository, transaction_repository, staff_repository
from app.services import user_service, transaction_service, auth_service


def get_user_repository():
    return user_repository


def get_transaction_repository():
    return transaction_repository


def get_staff_repository():
    return staff_repository


def get_user_service():
    return user_service


def get_transaction_service():
    return transaction_service


def get_auth_service():
    return auth_service
