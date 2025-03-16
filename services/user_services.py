from datetime import timedelta,datetime, timezone
from fastapi import status,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from fastapi.exceptions import HTTPException
from jose import jwt ,JWTError

from sqlalchemy.orm import Session

from schema.user_schema import UserCreate
from repositories.user_repository import UserRepository

from werkzeug.security import generate_password_hash ,check_password_hash




class UserService:
    def __init__(self,db: Session):
        self.db=db
        self.repository = UserRepository(db)


        self.SECRET_KEY='e5bddc5ac6b78059204847592d3c26079eb505af91f31640ffa74a8a8d7f9dbd'
        self.ALGORITHM='HS256'
        self.TOKEN_EXPIRE_MIN=30
        self.oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")

        
    def register_user(self,db: Session, user: UserCreate):
        return self.repository.create_user(db, user)
    



    def login_user(self,db:Session ,user_credentials:OAuth2PasswordRequestForm ):
        db_user=self.fetch_user_by_username(db,user_credentials.username)

        if db_user and check_password_hash(db_user.password,user_credentials.password):
            token=self.create_access_token(db_user.username,db_user.user_id,timedelta(minutes=20))
            print({'access_token':token,'token_type':'bearer'})
            return {'access_token':token,'token_type':'bearer'}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Username or Password')





    def fetch_user(db: Session, user_id: int):
        return UserRepository.get_user(db, user_id)




    def fetch_users(db: Session, skip: int = 0, limit: int = 10):
        return UserRepository.get_users(db, skip, limit)




    def fetch_user_by_username(self,db: Session, user_usename: str):
        return UserRepository.get_user_by_username(db, user_usename)    



    def create_access_token(self,username:str ,user_id,exp_delta:timedelta):
        encode={'sub':username,'id':user_id}
        expires=datetime.now(timezone.utc)+exp_delta
        encode.update({'exp':expires})

        return jwt.encode(encode,self.SECRET_KEY,algorithm=self.ALGORITHM)

