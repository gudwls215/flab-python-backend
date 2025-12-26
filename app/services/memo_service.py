"""
메모 Service 레이어
비즈니스 로직 및 예외 처리
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.memo import Memo
from app.schemas.memo import MemoCreate, MemoUpdate, MemoResponse, MemoListResponse
from app.repositories.memo_repository import memo_repository
from app.exceptions.memo_exceptions import MemoNotFoundException


class MemoService:
    """메모 비즈니스 로직 레이어"""
    
    def __init__(self):
        self.repository = memo_repository
    
    def create_memo(self, db: Session, memo_data: MemoCreate) -> MemoResponse:
        """
        새로운 메모 생성
        
        Args:
            db: 데이터베이스 세션
            memo_data: 메모 생성 데이터
            
        Returns:
            MemoResponse: 생성된 메모 응답
        """
        db_memo = self.repository.create_memo(db, memo_data)
        return MemoResponse.model_validate(db_memo)
    
    def get_memo(self, db: Session, memo_id: int) -> MemoResponse:
        """
        특정 메모 조회
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            
        Returns:
            MemoResponse: 메모 응답
            
        Raises:
            MemoNotFoundException: 메모를 찾을 수 없는 경우
        """
        db_memo = self.repository.get_memo_by_id(db, memo_id)
        if not db_memo:
            raise MemoNotFoundException(memo_id)
        return MemoResponse.model_validate(db_memo)
    
    def get_memos(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> MemoListResponse:
        """
        메모 목록 조회
        
        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 레코드 수
            limit: 조회할 최대 레코드 수
            
        Returns:
            MemoListResponse: 메모 목록 응답
        """
        memos, total = self.repository.get_memos(db, skip, limit)
        items = [MemoResponse.model_validate(memo) for memo in memos]
        return MemoListResponse(
            items=items,
            total=total,
            skip=skip,
            limit=limit
        )
    
    def update_memo(
        self, 
        db: Session, 
        memo_id: int, 
        memo_data: MemoUpdate
    ) -> MemoResponse:
        """
        메모 수정
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            memo_data: 수정할 메모 데이터
            
        Returns:
            MemoResponse: 수정된 메모 응답
            
        Raises:
            MemoNotFoundException: 메모를 찾을 수 없는 경우
        """
        db_memo = self.repository.update_memo(db, memo_id, memo_data)
        if not db_memo:
            raise MemoNotFoundException(memo_id)
        return MemoResponse.model_validate(db_memo)
    
    def delete_memo(self, db: Session, memo_id: int) -> None:
        """
        메모 삭제
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            
        Raises:
            MemoNotFoundException: 메모를 찾을 수 없는 경우
        """
        success = self.repository.delete_memo(db, memo_id)
        if not success:
            raise MemoNotFoundException(memo_id)


# Service 인스턴스 (싱글톤 패턴)
memo_service = MemoService()
