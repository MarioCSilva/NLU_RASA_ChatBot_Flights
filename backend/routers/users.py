
import sys
import os
import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import aux.utils as Utils
from aux import constants as Constants
import logging
import sql_app.schemas.feedback as FeedbackSchemas
import sql_app.schemas.users as UserSchemas
from sql_app.crud import crud_user, crud_feedback
from bot.connection_manager import manager
# import from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)


@router.post('/users/register',tags=['users'])
def register_new_user(new_user:UserSchemas.UserCreate, db: Session = Depends(Utils.get_db)):
    try:
        user = crud_user.create(db=db,user_data=new_user)
    except Exception as e:
        return Utils.create_response(status_code=e.status_code,success=False,errors=[e.message])
    return Utils.create_response(data=user,message="Sucess creating new user")

@router.post('/users/login',tags=['users'])
def login(user:UserSchemas.UserLogin, db:Session = Depends(Utils.get_db)):
    try:
        user = crud_user.get_user_by_username(db=db,user_data=user)
    except Exception as e:
        return Utils.create_response(status_code=e.status_code,success=False,errors=[e.message])
    return Utils.create_response(data=user,message="Sucessfully logged in")


@router.get('/users/help-required')
def get_usersRequiringHelp(db:Session = Depends(Utils.get_db)):
    users = manager.get_users_requiring_help()
    data = []
    for user in users:
        db_user = crud_user.get_userById(db,user)
        print(db_user)
        user_obj = UserSchemas.User(id=db_user.user_id,
            username=db_user.username,is_real_agent=db_user.is_real_agent)
        data.append(user_obj.dict())

    return Utils.create_response(data=data,message="Success getting users")