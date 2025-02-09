from fastapi import FastAPI
from routers import user_router

app = FastAPI()

# Include the user router
app.include_router(user_router.router)
