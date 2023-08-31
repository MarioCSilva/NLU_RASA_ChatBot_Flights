from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional

class FeedBackBase(BaseModel):
    user_id: int
    rating: int

    @validator('rating')
    def rating_must_be_between_range(cls,v):
        if not v>=1 and v<=5:
            raise ValueError("rating must be between 1 and 5") 
        return v

    
class FeedBackCreate(FeedBackBase):
    pass

class FeedBack(FeedBackBase):
    feedback_id: int
    timestamp : datetime
    
    class Config:
        orm_mode = True