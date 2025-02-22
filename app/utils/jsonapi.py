def universal_jsonapi(obj):
    if hasattr(obj, "__table__"):
        attributes = {}
        for column in obj.__table__.columns:
            if column.name == "id":
                continue

            value = getattr(obj, column.name)
            if value is not None and hasattr(value, "isoformat"):
                value = value.isoformat()

            attributes[column.name] = value
        type_name = obj.__tablename__

        return {"id": str(obj.id), "type": type_name, "attributes": attributes}
    else:
        attributes = {k: v for k, v in obj.__dict__.items() if k != "id" and not k.startswith("_")}
        type_name = type(obj).__name__.lower()

        return {"id": str(getattr(obj, "id", "")), "type": type_name, "attributes": attributes}


def jsonapi_response(result):
    if isinstance(result, list):
        return {"data": [universal_jsonapi(item) for item in result]}
    else:
        return {"data": universal_jsonapi(result)}
