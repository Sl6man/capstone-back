from models.user_model import UserCreate
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def add_new_user(self, user_data: UserCreate):
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")        
        return self.repository.create_user(user_data)

    def fetch_all_users(self, skip: int = 0, limit: int = 10):
        return self.repository.get_users(skip=skip, limit=limit)
