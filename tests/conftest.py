"""
pytest 설정 및 공통 fixture
테스트용 데이터베이스 세션 및 테스트 데이터 제공
"""
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.memo import Memo


# 테스트용 인메모리 SQLite 데이터베이스
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    테스트용 데이터베이스 세션 fixture
    각 테스트 함수마다 새로운 DB 세션 생성 및 정리
    """
    # 인메모리 SQLite 엔진 생성
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 세션 생성
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # 테이블 삭제
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_memo_data():
    """샘플 메모 데이터 fixture"""
    return {
        "title": "테스트 메모",
        "content": "테스트 메모 내용입니다."
    }


@pytest.fixture
def sample_memo_data_without_content():
    """내용이 없는 샘플 메모 데이터 fixture"""
    return {
        "title": "제목만 있는 메모"
    }


@pytest.fixture
def create_test_memo(db_session: Session):
    """테스트용 메모 생성 helper fixture"""
    def _create_memo(title: str = "테스트 메모", content: str = "테스트 내용") -> Memo:
        memo = Memo(title=title, content=content)
        db_session.add(memo)
        db_session.commit()
        db_session.refresh(memo)
        return memo
    return _create_memo
