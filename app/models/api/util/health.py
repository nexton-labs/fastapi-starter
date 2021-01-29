from pydantic import BaseModel


class Health(BaseModel):
    status: str = "OK"
    status_description: str = "OK"
    db_version: str = "Unknown"
