from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import auth
from app.routers.users import me_router
from app.routers.account import account
from app.routers.sessions import sessions
from app.routers.auth_me import me as auth_me
from app.core.config import settings
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(title="Stralix API", version="0.6.0")

app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(',') if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/api")
app.include_router(me_router, prefix="/api")
app.include_router(account, prefix="/api")
app.include_router(sessions, prefix="/api")
app.include_router(auth_me, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
