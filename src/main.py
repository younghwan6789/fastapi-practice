from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import root_router, users_router

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(root_router.router)
app.include_router(users_router.router)
