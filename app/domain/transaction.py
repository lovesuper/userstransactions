import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Numeric, Index
from sqlalchemy.orm import relationship

from app.domain import utcnow
from app.domain.enums import OperationType
from app.domain.mixins import JSONAPIMixin, Base


class Transaction(JSONAPIMixin, Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index('ix_transactions_user_id', "user_id"),
    )

    amount = Column(Numeric)
    created = Column(DateTime, default=utcnow)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    operation_type = Column(Enum(OperationType))
    staff_id = Column(String(36), ForeignKey("staff.id"))
    user_id = Column(String(36), ForeignKey("users.id"))

    user = relationship("User", back_populates="transactions")
