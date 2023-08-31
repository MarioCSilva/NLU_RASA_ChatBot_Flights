from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# TODO: add validator for optional types in sender and receiver
class MessageBase(BaseModel):
    receiver: Optional[int] = None
    sender: Optional[int] = None
    content: str
    content_type: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: int
    timestamp : datetime
    
    class Config:
        orm_mode = True
