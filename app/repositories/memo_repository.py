"""
메모 Repository 레이어
데이터베이스 CRUD 연산 담당
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.memo import Memo
from app.schemas.memo import MemoCreate, MemoUpdate


class MemoRepository:
    """메모 데이터베이스 접근 레이어"""
    
    def create_memo(self, db: Session, memo_data: MemoCreate) -> Memo:
        """
        새로운 메모 생성
        
        Args:
            db: 데이터베이스 세션
            memo_data: 메모 생성 데이터
            
        Returns:
            Memo: 생성된 메모 객체
        """
        db_memo = Memo(
            title=memo_data.title,
            content=memo_data.content
        )
        db.add(db_memo)
        db.commit()
        db.refresh(db_memo)
        return db_memo
    
    def get_memo_by_id(self, db: Session, memo_id: int) -> Optional[Memo]:
        """
        ID로 특정 메모 조회
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            
        Returns:
            Optional[Memo]: 메모 객체 또는 None
        """
        return db.query(Memo).filter(Memo.id == memo_id).first()
    
    def get_memos(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[List[Memo], int]:
        """
        메모 목록 조회 (페이징 지원)
        
        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 레코드 수
            limit: 조회할 최대 레코드 수
            
        Returns:
            tuple[List[Memo], int]: (메모 목록, 전체 메모 수)
        """
        total = db.query(func.count(Memo.id)).scalar()
        memos = (
            db.query(Memo)
            .order_by(Memo.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return memos, total
    
    def update_memo(
        self, 
        db: Session, 
        memo_id: int, 
        memo_data: MemoUpdate
    ) -> Optional[Memo]:
        """
        메모 수정
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            memo_data: 수정할 메모 데이터
            
        Returns:
            Optional[Memo]: 수정된 메모 객체 또는 None
        """
        db_memo = self.get_memo_by_id(db, memo_id)
        if not db_memo:
            return None
        
        # 제공된 필드만 업데이트
        update_data = memo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_memo, field, value)
        
        db.commit()
        db.refresh(db_memo)
        return db_memo
    
    def delete_memo(self, db: Session, memo_id: int) -> bool:
        """
        메모 삭제
        
        Args:
            db: 데이터베이스 세션
            memo_id: 메모 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        db_memo = self.get_memo_by_id(db, memo_id)
        if not db_memo:
            return False
        
        db.delete(db_memo)
        db.commit()
        return True


# Repository 인스턴스 (싱글톤 패턴)
memo_repository = MemoRepository()
