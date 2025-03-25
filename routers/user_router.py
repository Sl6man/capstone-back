from fastapi import APIRouter, HTTPException ,Depends ,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from data.db_config import SessionLocal,engine
from sqlalchemy.orm import Session

from schema.user_schema import UserCreate, UserResponse,Token,GroupCreate ,RoleCreate,GroupResponse,RoleResponse,UsersInfoResonse
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


@router.get('/userInfo/{user_id}' ,response_model=UserCreate)
async def get_user_info( user_id:int,db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.fetch_user(db,user_id)

@router.get('/usersInfoTable',response_model=list[UsersInfoResonse])
async def get_users_info_for_table(db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.fetch_users_for_table(db)   

@router.get('/groups',response_model=list[GroupResponse],status_code=status.HTTP_200_OK)
async def get_groups(db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.fetch_all_groups(db)


@router.get('/role',response_model=list[RoleResponse],status_code=status.HTTP_200_OK)
async def get_roles(db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.fetch_all_roles(db)



#-----------------------POST-------------------------------------
@router.post("/createUser", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print('---=---')
    print(user)
    user_service = UserService(db)
    return user_service.register_user(db,user)

@router.post('/login',response_model=Token)
async def login(user_credentials:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.login_user(db,user_credentials)


@router.post('/groupCreate',status_code=status.HTTP_201_CREATED)
async def create_group(group:GroupCreate,db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_group(db,group)





@router.post('/role')
async def create_role(role:RoleCreate,db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_role(db,role)
    






'''
@router.get('/u')
async def getuser(db:Session=Depends(get_db), id : int):
    user_service = UserService(db)
    return  user_service.fetch_user(db,id)'''