from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from data.db_config import Base

class User(Base):
    __tablename__= "user"

    user_id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    job_title=Column(String,nullable=True)
    fname=Column(String,nullable=False)
    lname=Column(String,nullable=False)

    group_id=Column(Integer,ForeignKey('group.group_id'),nullable=True)
    role_id=Column(Integer,ForeignKey('role.role_id'),nullable=False)

    role=relationship('Role')
    group=relationship('Group')
   
    
class Group(Base):
    __tablename__='group'

    group_id=Column(Integer,primary_key=True,autoincrement=True)    
    name=Column(String,unique=True,nullable=False)



class Role(Base):
    __tablename__='role'


    role_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,unique=True,nullable=False)
    description=Column(String,nullable=False)


