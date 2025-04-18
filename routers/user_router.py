from fastapi import APIRouter, HTTPException ,Depends ,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from data.db_config import SessionLocal,engine
from sqlalchemy.orm import Session

from schema.user_schema import UserCreate, UserResponse,Token,GroupCreate ,RoleCreate,GroupResponse,RoleResponse, UserUpdate,UsersInfoResonse,UserEditResponse

from security.permissions import get_current_user_role
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

#-----------------------GET-------------------------------------
@router.get('/user/info/{user_id}' ,response_model=UserEditResponse)
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

# update the URLs with the best practices 
# for example /createUser -> /create/user

#-----------------------POST-------------------------------------
@router.post("/create/user", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
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
    
#------------------------------------test-------------------------------------------------------------------
@router.get('/test')
def test_method(role: str = Depends(get_current_user_role), db:Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.test_use(role_id=role)


#-----------------patch---------------------

@router.patch("/edit/user/{user_id}")
async def edit_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):

   
    user_service = UserService(db)
    updated_user = user_service.edit_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


#-----------------delete---------------------

@router.delete("/delete/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    user_service = UserService(db)
    deleted_user = user_service.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
