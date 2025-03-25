from sqlalchemy.orm import  Session
from schema.user_schema import UserCreate,GroupCreate,RoleCreate
from models.user_model import User,Group,Role
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
            lname=user.lname,
            group_id=user.group_id,
            role_id=user.role_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user    


    def create_group(self,db:Session,group:GroupCreate):
        db_group=Group(
            name=group.name
        )
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group
    


    def create_role(self,db:Session,role:RoleCreate):
        db_role=Role(
            name=role.name,
            description=role.description
        )
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role


#------------------------------------get ---------------------------------------------------

    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_username(db: Session, user_username: str):
        return db.query(User).filter(User.username == user_username).first()    

    def get_users_for_table(db:Session):
        return db.query(User).join(Group).join(Role).all()




    def get_group_by_id(db: Session, group_id: str):
        return db.query(Group).filter(Group.group_id == group_id).first()  

    def get_group_by_name(db:Session,group_name:str):
        return db.query(Group).filter(Group.name == group_name).first()
    
    def get_all_groups(db:Session):
        return db.query(Group).all()



    def get_role_by_id(db: Session, role_id: str):
        return db.query(Role).filter(Role.role_id == role_id).first()  

    def get_all_roles(db:Session):
        return db.query(Role).all()

    def get_users(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
