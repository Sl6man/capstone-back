from fastapi import APIRouter, HTTPException ,Depends ,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from data.db_config import SessionLocal,engine
from sqlalchemy.orm import Session

from schema.user_schema import UserCreate, UserResponse,Token
from services.user_services import UserService

from typing import Annotated



router = APIRouter(prefix="/users", tags=["users"])
#user_service = UserService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/e")
def hel():
    return({"message":"hello111111"})

@router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print('---=---')
    print(user)
    user_service = UserService(db)
    return user_service.register_user(db,user)

@router.post('/login',response_model=Token)
async def login(user_credentials:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.login_user(db,user_credentials)
'''
@router.get('/u')
async def getuser(db:Session=Depends(get_db), id : int):
    user_service = UserService(db)
    return  user_service.fetch_user(db,id)'''