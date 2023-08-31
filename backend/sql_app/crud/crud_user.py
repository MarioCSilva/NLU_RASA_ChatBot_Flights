import sql_app.schemas.users as UserSchemas
import logging 
from sqlalchemy.orm import Session
from  sql_app import models 
from aux.exceptions import CustomException
# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

def create(db: Session, user_data: UserSchemas.UserCreate):
    user_obj = db.query(models.User).filter(models.User.username == user_data.username).first()
    if user_obj: 
        raise CustomException(message="User Already Exists")
    db_user =  models.User(
        username=user_data.username,
        is_real_agent=user_data.is_real_agent)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
   
    return  UserSchemas.User(id=db_user.user_id,
    username=db_user.username,is_real_agent=db_user.is_real_agent).dict()

def get_user_by_username(db: Session,  user_data: UserSchemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not db_user:
        raise CustomException(message="User Does not Exists")
    return  UserSchemas.User(id=db_user.user_id,
    username=db_user.username,is_real_agent=db_user.is_real_agent).dict()

def get_userById(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        raise CustomException(message="User Does not Exists")
    return  db_user