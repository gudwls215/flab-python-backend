"""
메모 ORM 모델
SQLAlchemy를 사용한 데이터베이스 테이블 정의
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class Memo(Base):
    """메모 테이블 모델"""
    
    __tablename__ = "memos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="메모 제목")
    content = Column(Text, nullable=True, comment="메모 내용")
    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        comment="생성 일시"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="수정 일시"
    )
    
    def __repr__(self) -> str:
        return f"<Memo(id={self.id}, title='{self.title}')>"
