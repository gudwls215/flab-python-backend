"""
메모 Service 유닛 테스트
비즈니스 로직 및 예외 처리 테스트
"""
import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from app.services.memo_service import memo_service
from app.schemas.memo import MemoCreate, MemoUpdate, MemoResponse, MemoListResponse
from app.exceptions.memo_exceptions import MemoNotFoundException


class TestMemoService:
    """메모 Service 테스트"""
    
    def test_create_memo(self, db_session: Session, sample_memo_data):
        """메모 생성 서비스 테스트"""
        # Given
        memo_data = MemoCreate(**sample_memo_data)
        
        # When
        result = memo_service.create_memo(db_session, memo_data)
        
        # Then
        assert isinstance(result, MemoResponse)
        assert result.title == sample_memo_data["title"]
        assert result.content == sample_memo_data["content"]
        assert result.id is not None
    
    def test_get_memo_success(self, db_session: Session, create_test_memo):
        """메모 조회 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="조회 테스트", content="조회 내용")
        
        # When
        result = memo_service.get_memo(db_session, test_memo.id)
        
        # Then
        assert isinstance(result, MemoResponse)
        assert result.id == test_memo.id
        assert result.title == test_memo.title
        assert result.content == test_memo.content
    
    def test_get_memo_not_found(self, db_session: Session):
        """메모 조회 실패 테스트 (NotFoundException)"""
        # When & Then
        with pytest.raises(MemoNotFoundException) as exc_info:
            memo_service.get_memo(db_session, 999)
        
        assert exc_info.value.memo_id == 999
        assert "999" in str(exc_info.value)
    
    def test_get_memos_empty(self, db_session: Session):
        """빈 메모 목록 조회 테스트"""
        # When
        result = memo_service.get_memos(db_session)
        
        # Then
        assert isinstance(result, MemoListResponse)
        assert len(result.items) == 0
        assert result.total == 0
        assert result.skip == 0
        assert result.limit == 100
    
    def test_get_memos(self, db_session: Session, create_test_memo):
        """메모 목록 조회 테스트"""
        # Given
        create_test_memo(title="메모 1", content="내용 1")
        create_test_memo(title="메모 2", content="내용 2")
        create_test_memo(title="메모 3", content="내용 3")
        
        # When
        result = memo_service.get_memos(db_session, skip=0, limit=10)
        
        # Then
        assert isinstance(result, MemoListResponse)
        assert len(result.items) == 3
        assert result.total == 3
        assert all(isinstance(item, MemoResponse) for item in result.items)
    
    def test_get_memos_with_pagination(self, db_session: Session, create_test_memo):
        """페이징을 사용한 메모 목록 조회 테스트"""
        # Given
        for i in range(5):
            create_test_memo(title=f"메모 {i+1}", content=f"내용 {i+1}")
        
        # When
        result = memo_service.get_memos(db_session, skip=1, limit=2)
        
        # Then
        assert len(result.items) == 2
        assert result.total == 5
        assert result.skip == 1
        assert result.limit == 2
    
    def test_update_memo_success(self, db_session: Session, create_test_memo):
        """메모 수정 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = MemoUpdate(title="수정된 제목", content="수정된 내용")
        
        # When
        result = memo_service.update_memo(db_session, test_memo.id, update_data)
        
        # Then
        assert isinstance(result, MemoResponse)
        assert result.id == test_memo.id
        assert result.title == "수정된 제목"
        assert result.content == "수정된 내용"
    
    def test_update_memo_partial(self, db_session: Session, create_test_memo):
        """메모 부분 수정 테스트"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = MemoUpdate(title="수정된 제목")
        
        # When
        result = memo_service.update_memo(db_session, test_memo.id, update_data)
        
        # Then
        assert result.title == "수정된 제목"
        assert result.content == "원본 내용"
    
    def test_update_memo_not_found(self, db_session: Session):
        """메모 수정 실패 테스트 (NotFoundException)"""
        # Given
        update_data = MemoUpdate(title="수정된 제목")
        
        # When & Then
        with pytest.raises(MemoNotFoundException) as exc_info:
            memo_service.update_memo(db_session, 999, update_data)
        
        assert exc_info.value.memo_id == 999
    
    def test_delete_memo_success(self, db_session: Session, create_test_memo):
        """메모 삭제 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="삭제할 메모", content="삭제할 내용")
        
        # When
        memo_service.delete_memo(db_session, test_memo.id)
        
        # Then
        # 삭제 후 조회 시 예외 발생 확인
        with pytest.raises(MemoNotFoundException):
            memo_service.get_memo(db_session, test_memo.id)
    
    def test_delete_memo_not_found(self, db_session: Session):
        """메모 삭제 실패 테스트 (NotFoundException)"""
        # When & Then
        with pytest.raises(MemoNotFoundException) as exc_info:
            memo_service.delete_memo(db_session, 999)
        
        assert exc_info.value.memo_id == 999
