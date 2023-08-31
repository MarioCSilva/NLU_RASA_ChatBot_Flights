from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    is_real_agent: bool
    #balance: float
class UserCreate(UserBase):

    pass
class UserLogin(BaseModel):
    username: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
