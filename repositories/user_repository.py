from sqlalchemy.orm import  Session
from data.db_config import get_db
from models.user_model import UserCreate
from schema.user_schema import User

class UserRepository:
    def __init__(self):
        self.db: Session = next(get_db())

    def create_user(self, user: UserCreate):
        db_user = User(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def close_db(self):
        self.db.close()
