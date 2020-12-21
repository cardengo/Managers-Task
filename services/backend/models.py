from pydantic import BaseModel


class UserAuthModel(BaseModel):
    user_id: str
    password: str
