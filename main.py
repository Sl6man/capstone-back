from contextlib import asynccontextmanager
from fastapi import FastAPI
from data.mongo_config import check_mongo_connection
from models.user_model import Role
from routers import scraper_router, user_router,media_router
from data.db_config import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware 
from fastapi_jwt import JwtAccessBearer
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

# Recreate tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")





app = FastAPI()

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
app.include_router(media_router.router)
