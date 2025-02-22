import uuid

from sqlalchemy import Column, String, DateTime, Boolean, Index
from sqlalchemy.orm import relationship

from app.domain import utcnow
from app.domain.mixins import JSONAPIMixin, Base


class User(JSONAPIMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('ix_users_username', "username"),
        Index('ix_users_verified', "verified"),
        Index('ix_users_is_deleted', "is_deleted"),
    )

    city = Column(String)
    country = Column(String)
    created = Column(DateTime, default=utcnow)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    is_deleted = Column(Boolean, default=False)
    last_name = Column(String)
    modified = Column(DateTime, default=utcnow, onupdate=utcnow)
    username = Column(String, unique=True, index=True)
    verified = Column(DateTime, nullable=True)

    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )
