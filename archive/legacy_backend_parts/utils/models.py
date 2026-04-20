from pydantic import BaseModel

class MessageData(BaseModel):
    message: str
    user_id: str
    username: str


class DeleteData(BaseModel):
    user_id: str