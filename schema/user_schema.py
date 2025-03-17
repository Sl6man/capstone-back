
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    
    username:str
    email:EmailStr
    job_title:str | None=None
    fname:str
    lname:str
    password:str
    group_id: int
    role_id: int
 
class GroupCreate(BaseModel):
    name:str


class RoleCreate(BaseModel):
    name:str
    description:str

class Token(BaseModel):
    access_token:str
    token_type:str



class UserResponse(BaseModel):
    user_id:int


    class Config:
        from_attributes = True    



