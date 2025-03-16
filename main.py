from fastapi import FastAPI
from routers import user_router
from data.db_config import engine, Base
from fastapi.middleware.cors import CORSMiddleware 
from fastapi_jwt import JwtAccessBearer

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Recreate tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")


# Include the user router
app.include_router(user_router.router)
