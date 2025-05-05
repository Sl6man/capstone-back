from datetime import timedelta,datetime, timezone
from fastapi import status,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from fastapi.exceptions import HTTPException
from jose import jwt 
from sqlalchemy.orm import Session

from schema.user_schema import UserCreate,GroupCreate,RoleCreate, UserUpdate,UsersInfoResonse
from repositories.user_repository import UserRepository

from werkzeug.security import generate_password_hash ,check_password_hash

from security.permissions import has_permission
from fastapi import HTTPException



class UserService:
    def __init__(self,db: Session):
        self.db=db
        self.repository = UserRepository(db)

        
        self.SECRET_KEY='e5bddc5ac6b78059204847592d3c26079eb505af91f31640ffa74a8a8d7f9dbd'
        self.ALGORITHM='HS256'
        self.TOKEN_EXPIRE_MIN=30
        self.oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")

        
    def register_user(self,db: Session, user: UserCreate):
        
        group=self.fetch_group_by_id(db,user.group_id)
        if not group :
            raise HTTPException(status_code=400 ,detail='Group does not exist')


        role=self.fetch_role_by_id(db,user.role_id)
        if not role:
            raise HTTPException(status_code=400 ,detail='Role does not exist')
        

        username=self.fetch_user_by_username(db,user.username)
        if username :
            raise HTTPException(status_code=400 ,detail='Username Already Exists')

        
        email = self.fetch_user_by_email(db, user.email)     
        if email:
            raise HTTPException(status_code=400, detail='Email Already Exists')

        return self.repository.create_user(db, user)  




    
    

    def login_user(self,db:Session ,user_credentials:OAuth2PasswordRequestForm ):
        db_user=self.fetch_user_by_username(db,user_credentials.username)

        if db_user and check_password_hash(db_user.password,user_credentials.password):            
            role_name = role=self.fetch_role_by_id(db,db_user.role_id).name
            
            token=self.create_access_token(db_user.username,db_user.user_id, role_name,timedelta(minutes=20))
            print({'access_token':token,'token_type':'bearer'})
            return {'access_token':token,'token_type':'bearer'}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Username or Password')

    def create_access_token(self,username:str ,user_id, role_id:int, exp_delta:timedelta):
        encode={'sub':username,'id':user_id, 'role_id': role_id}
        expires=datetime.now(timezone.utc)+exp_delta
        encode.update({'exp':expires})

        return jwt.encode(encode,self.SECRET_KEY,algorithm=self.ALGORITHM)

    def create_group(self,db:Session,group:GroupCreate):
        group_name=self.fetch_group_by_name(db,group.name)
        if group_name:
            raise HTTPException(status_code=400 , detail='Group Already Exists')

        return self.repository.create_group(db, group)
    
    def create_role(self,db:Session,role:RoleCreate):
        return self.repository.create_role(db,role)





    def fetch_all_groups(self,db:Session):
        return UserRepository.get_all_groups(db)




    def fetch_user(self, db: Session, user_id: int):
        user = UserRepository.get_user(db, user_id)

        if not user:
           raise HTTPException(status_code=404, detail="User not found")
        return user


    def fetch_user_by_username(self,db: Session, user_usename: str):
        return UserRepository.get_user_by_username(db, user_usename)    

    def fetch_user_by_email(self,db: Session,email:str):
        return UserRepository.get_user_by_email(email)   
 
    
    
    
    
    def fetch_users_for_table(self,db:Session):
        users=UserRepository.get_users_for_table(db)

        users_list=[]
        for user in users:
            
            user_info=UsersInfoResonse(
                id=user.user_id,
                name=f'{user.fname} {user.lname}',
                email=user.email,
                group=user.group.name,
                role=user.role.name,
            )
            users_list.append(user_info)

        return users_list    



    def fetch_group_by_id(self,db: Session, group_id: str):
        return UserRepository.get_group_by_id(db, group_id)    

    def fetch_group_by_name(self,db: Session, group_name: str):
        return UserRepository.get_group_by_name(db, group_name)



    def fetch_role_by_id(self,db: Session, role_id: str):
        return UserRepository.get_role_by_id(db, role_id)    

    def fetch_all_roles(self,db:Session):
        return UserRepository.get_all_roles(db)
    
    def fetch_user_by_email(self, db: Session, email: str):  #write by Fahad
        return UserRepository.get_user_by_email(db, email)   

    
#-------------- test--------------------
    
    def test_use(self, role_id:str):
        print(2)
        if not has_permission("Admin", "team_page", "edit"):
            raise HTTPException(status_code=403, detail="Permission denied: Cannot edit this page")
        
        print(role_id)
        return True

#----------------------- patch---------------------------------


    def edit_user(self, db: Session, user_id: int, user_update: UserUpdate):


        email=self.fetch_user_by_email(db,user_update.email)
        if email:
            raise HTTPException(status_code=409,detail="Email already exists")

        return UserRepository.update_user(db, user_id, user_update)
    
    




#-----------------delete-----------------------------------------------


    def delete_user(self, db: Session, user_id: int):
        return self.repository.delete_user(db, user_id)



