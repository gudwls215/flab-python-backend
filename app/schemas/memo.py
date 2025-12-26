"""
메모 Pydantic 스키마
API 요청/응답 데이터 검증 및 직렬화
"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MemoBase(BaseModel):
    """메모 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200, description="메모 제목")
    content: Optional[str] = Field(None, max_length=5000, description="메모 내용")


class MemoCreate(MemoBase):
    """메모 생성 요청 스키마"""
    pass


class MemoUpdate(BaseModel):
    """메모 수정 요청 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="메모 제목")
    content: Optional[str] = Field(None, max_length=5000, description="메모 내용")


class MemoResponse(MemoBase):
    """메모 응답 스키마"""
    id: int = Field(..., description="메모 ID")
    created_at: datetime = Field(..., description="생성 일시")
    updated_at: datetime = Field(..., description="수정 일시")
    
    model_config = ConfigDict(from_attributes=True)


class MemoListResponse(BaseModel):
    """메모 목록 응답 스키마"""
    items: list[MemoResponse] = Field(..., description="메모 목록")
    total: int = Field(..., description="전체 메모 수")
    skip: int = Field(..., description="건너뛴 메모 수")
    limit: int = Field(..., description="조회한 메모 수")
