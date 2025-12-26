"""
API v1 패키지
"""
from fastapi import APIRouter
from app.api.v1.endpoints import memos

api_router = APIRouter()

# 메모 엔드포인트 등록
api_router.include_router(
    memos.router,
    prefix="/memos",
    tags=["memos"]
)
