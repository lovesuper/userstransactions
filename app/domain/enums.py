import enum


class UserRole(enum.Enum):
    staff = "staff"
    user = "user"


class OperationType(enum.Enum):
    accrual = "accrual"
    writeoff = "writeoff"
