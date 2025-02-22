import uuid

from sqlalchemy import Column, String

from app.domain.mixins import JSONAPIMixin, Base


class Staff(JSONAPIMixin, Base):
    __tablename__ = "staff"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    login = Column(String, unique=True, index=True)
