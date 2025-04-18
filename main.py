from contextlib import asynccontextmanager
from fastapi import FastAPI
from models.user_model import Role
from routers import scraper_router, user_router
from data.db_config import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware 
from fastapi_jwt import JwtAccessBearer
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

# Recreate tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")


def create_default_roles():
    db: Session = SessionLocal()
    default_roles = ["admin", "editor", "viewer"]
    
    # Check if roles exist
    existing_roles = db.query(Role).count()
    if existing_roles == 0:
        for role in default_roles:
            db.add(Role(name=role))
        db.commit()
    
    db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_default_roles()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user router
app.include_router(user_router.router)
app.include_router(scraper_router.router)
