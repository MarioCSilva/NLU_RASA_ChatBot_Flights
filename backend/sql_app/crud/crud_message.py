from sqlite3 import Timestamp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import aux.utils as Utils
import sql_app.schemas.messages as MessageSchemas
from sqlalchemy.orm import Session
from sqlalchemy import or_
from  sql_app import models 
from aux.exceptions import CustomException

def create(message_data: MessageSchemas.MessageCreate, db:Session):
   
    msg_obj = models.Message(
        receiver= message_data.receiver, sender=message_data.sender,
        content=message_data.content, content_type=message_data.content_type
    )

    db.add(msg_obj)
    db.commit()
    db.refresh(msg_obj)
   
    return MessageSchemas.Message(**msg_obj.__dict__).dict()

def get_all(user_id: int, db:Session):
    
    msgs = db.query(models.Message).filter(or_(models.Message.receiver == user_id, models.Message.sender == user_id)).all()
    return [MessageSchemas.Message(**msg.__dict__).dict() for msg in msgs]