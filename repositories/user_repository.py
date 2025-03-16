from sqlalchemy.orm import  Session
from schema.user_schema import UserCreate
from models.user_model import User
from werkzeug.security import generate_password_hash ,check_password_hash
class UserRepository:
    def __init__(self,db:Session):
        self.db = db

    
    def create_user(self,db: Session, user: UserCreate):
        db_user = User(
            username=user.username,
            email=user.email,
            password=generate_password_hash(user.password),
            job_title=user.job_title,
            fname=user.fname,
            lname=user.lname
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user    

    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_username(db: Session, user_username: str):
        return db.query(User).filter(User.username == user_username).first()    

    def get_users(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
