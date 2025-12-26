"""
FastAPI 메인 애플리케이션
메모장 CRUD API 서버
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import api_router
from app.exceptions.memo_exceptions import MemoNotFoundException


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI와 PostgreSQL을 활용한 메모장 CRUD API",
    debug=settings.DEBUG
)


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 전역 예외 핸들러
@app.exception_handler(MemoNotFoundException)
async def memo_not_found_exception_handler(
    request: Request, 
    exc: MemoNotFoundException
) -> JSONResponse:
    """메모를 찾을 수 없을 때 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "memo_id": exc.memo_id
        }
    )


# API 라우터 등록
app.include_router(
    api_router,
    prefix="/api/v1"
)


# Health check 엔드포인트
@app.get("/", tags=["health"])
async def root():
    """서버 상태 확인"""
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health", tags=["health"])
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
