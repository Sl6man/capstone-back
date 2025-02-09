from fastapi import APIRouter, HTTPException
from models.user_model import UserCreate, UserResponse
from services.user_services import UserService

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    try:
        return user_service.add_new_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10):
    return user_service.fetch_all_users(skip=skip, limit=limit)
