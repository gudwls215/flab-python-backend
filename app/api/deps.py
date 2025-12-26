"""
API 의존성
FastAPI 엔드포인트에서 사용할 공통 의존성
"""
from typing import Generator
from sqlalchemy.orm import Session

from app.database import get_db


def get_db_session() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 의존성
    FastAPI 엔드포인트에서 DB 세션을 주입받기 위해 사용
    
    Yields:
        Session: SQLAlchemy 데이터베이스 세션
    """
    yield from get_db()
