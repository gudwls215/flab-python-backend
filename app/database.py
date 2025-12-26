"""
데이터베이스 연결 및 세션 관리
SQLAlchemy 엔진 및 세션 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings


# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,  # SQL 쿼리 로깅 (DEBUG 모드에서만)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 생성 (모든 ORM 모델의 부모 클래스)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 의존성
    FastAPI 엔드포인트에서 사용할 DB 세션 제공
    
    Yields:
        Session: SQLAlchemy 데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    데이터베이스 초기화
    모든 테이블 생성 (개발 환경용, 프로덕션에서는 Alembic 사용)
    """
    Base.metadata.create_all(bind=engine)
