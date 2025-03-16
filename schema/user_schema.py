
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    user_id: Optional[int] = None
    username:str
    email:EmailStr
    job_title:str | None=None
    fname:str
    lname:str
    password:str
 
class UserResponse(BaseModel):
    user_id:int


    class Config:
        from_attributes = True    


class Token(BaseModel):
    access_token:str
    token_type:str

