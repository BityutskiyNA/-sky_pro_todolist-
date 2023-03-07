from pydantic import BaseModel, Field
from typing import Optional

class Chat(BaseModel):
    id: int
    # username: str | None = None
    username: Optional[str] = None


class MessageFrom(BaseModel):
    id: int
    # username: str | None = None
    username: Optional[str] = None


class Message(BaseModel):
    message_id: int
    from_:MessageFrom = Field(... , alias='from')
    chat: Chat
    # text: str | None = None
    text: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj] = []



class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
