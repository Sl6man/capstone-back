
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
 
class UsersInfoResonse(BaseModel):
    id:int
    name:str
    email:EmailStr
    group:str
    role:str



class GroupCreate(BaseModel):
    name:str


class GroupResponse(BaseModel):
   group_id:int
   name:str



class RoleCreate(BaseModel):
    name:str
    description:str

class RoleResponse(BaseModel):
    role_id:int
    name:str
    description:str






class Token(BaseModel):
    access_token:str
    token_type:str



class UserResponse(BaseModel):
    username:str


    class Config:
        from_attributes = True    



