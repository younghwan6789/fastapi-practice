from fastapi import FastAPI

from src.routers import root_router, users_router

app = FastAPI()

app.include_router(root_router.router)
app.include_router(users_router.router)
