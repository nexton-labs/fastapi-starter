import uuid

from pydantic import BaseModel


class Token(BaseModel):
    access_token: bytes
    token_type: str

    @property
    def authorization(self) -> str:
        return f"{self.token_type.capitalize()} {self.access_token.decode('utf-8')}"


class TokenData(BaseModel):
    user_id: uuid.UUID
