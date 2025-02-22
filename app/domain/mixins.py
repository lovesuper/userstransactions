from sqlalchemy.orm import declarative_base

Base = declarative_base()


class JSONAPIMixin:
    # noinspection PyUnresolvedReferences
    def jsonify(self):
        attributes = {}
        for col in self.__table__.columns:
            if col.name == "id":
                continue

            value = getattr(self, col.name)
            if value is not None and hasattr(value, "isoformat"):
                value = value.isoformat()

            attributes[col.name] = value

        return {"id": str(self.id), "type": self.__tablename__, "attributes": attributes}
