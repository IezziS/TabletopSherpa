from fastapi import FastAPI
from backend.routers import chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    chat_router.router,
    prefix='/chat',
    tags=['chat']
)
