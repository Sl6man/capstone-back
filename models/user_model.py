from sqlalchemy import Column, Integer, String

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
   
    