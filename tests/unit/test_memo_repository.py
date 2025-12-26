"""
메모 Repository 유닛 테스트
데이터베이스 CRUD 로직 테스트
"""
import pytest
from sqlalchemy.orm import Session

from app.repositories.memo_repository import memo_repository
from app.schemas.memo import MemoCreate, MemoUpdate
from app.models.memo import Memo


class TestMemoRepository:
    """메모 Repository 테스트"""
    
    def test_create_memo(self, db_session: Session, sample_memo_data):
        """메모 생성 테스트"""
        # Given
        memo_data = MemoCreate(**sample_memo_data)
        
        # When
        created_memo = memo_repository.create_memo(db_session, memo_data)
        
        # Then
        assert created_memo.id is not None
        assert created_memo.title == sample_memo_data["title"]
        assert created_memo.content == sample_memo_data["content"]
        assert created_memo.created_at is not None
        assert created_memo.updated_at is not None
    
    def test_create_memo_without_content(self, db_session: Session, sample_memo_data_without_content):
        """내용 없이 메모 생성 테스트"""
        # Given
        memo_data = MemoCreate(**sample_memo_data_without_content)
        
        # When
        created_memo = memo_repository.create_memo(db_session, memo_data)
        
        # Then
        assert created_memo.id is not None
        assert created_memo.title == sample_memo_data_without_content["title"]
        assert created_memo.content is None
    
    def test_get_memo_by_id(self, db_session: Session, create_test_memo):
        """ID로 메모 조회 테스트"""
        # Given
        test_memo = create_test_memo(title="조회 테스트", content="조회 테스트 내용")
        
        # When
        found_memo = memo_repository.get_memo_by_id(db_session, test_memo.id)
        
        # Then
        assert found_memo is not None
        assert found_memo.id == test_memo.id
        assert found_memo.title == test_memo.title
        assert found_memo.content == test_memo.content
    
    def test_get_memo_by_id_not_found(self, db_session: Session):
        """존재하지 않는 메모 조회 테스트"""
        # When
        found_memo = memo_repository.get_memo_by_id(db_session, 999)
        
        # Then
        assert found_memo is None
    
    def test_get_memos_empty(self, db_session: Session):
        """빈 메모 목록 조회 테스트"""
        # When
        memos, total = memo_repository.get_memos(db_session)
        
        # Then
        assert len(memos) == 0
        assert total == 0
    
    def test_get_memos(self, db_session: Session, create_test_memo):
        """메모 목록 조회 테스트"""
        # Given
        memo1 = create_test_memo(title="메모 1", content="내용 1")
        memo2 = create_test_memo(title="메모 2", content="내용 2")
        memo3 = create_test_memo(title="메모 3", content="내용 3")
        
        # When
        memos, total = memo_repository.get_memos(db_session)
        
        # Then
        assert len(memos) == 3
        assert total == 3
        # 메모가 조회되는지 확인 (순서는 created_at에 따라 달라질 수 있음)
        memo_ids = {memo.id for memo in memos}
        assert memo1.id in memo_ids
        assert memo2.id in memo_ids
        assert memo3.id in memo_ids
    
    def test_get_memos_with_pagination(self, db_session: Session, create_test_memo):
        """페이징을 사용한 메모 목록 조회 테스트"""
        # Given
        for i in range(5):
            create_test_memo(title=f"메모 {i+1}", content=f"내용 {i+1}")
        
        # When
        memos, total = memo_repository.get_memos(db_session, skip=2, limit=2)
        
        # Then
        assert len(memos) == 2
        assert total == 5
        # skip=2, limit=2이므로 2개의 메모가 반환되어야 함
    
    def test_update_memo(self, db_session: Session, create_test_memo):
        """메모 수정 테스트"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = MemoUpdate(title="수정된 제목", content="수정된 내용")
        
        # When
        updated_memo = memo_repository.update_memo(db_session, test_memo.id, update_data)
        
        # Then
        assert updated_memo is not None
        assert updated_memo.id == test_memo.id
        assert updated_memo.title == "수정된 제목"
        assert updated_memo.content == "수정된 내용"
    
    def test_update_memo_partial(self, db_session: Session, create_test_memo):
        """메모 부분 수정 테스트 (제목만)"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = MemoUpdate(title="수정된 제목")
        
        # When
        updated_memo = memo_repository.update_memo(db_session, test_memo.id, update_data)
        
        # Then
        assert updated_memo is not None
        assert updated_memo.title == "수정된 제목"
        assert updated_memo.content == "원본 내용"  # 내용은 그대로
    
    def test_update_memo_not_found(self, db_session: Session):
        """존재하지 않는 메모 수정 테스트"""
        # Given
        update_data = MemoUpdate(title="수정된 제목")
        
        # When
        updated_memo = memo_repository.update_memo(db_session, 999, update_data)
        
        # Then
        assert updated_memo is None
    
    def test_delete_memo(self, db_session: Session, create_test_memo):
        """메모 삭제 테스트"""
        # Given
        test_memo = create_test_memo(title="삭제할 메모", content="삭제할 내용")
        
        # When
        result = memo_repository.delete_memo(db_session, test_memo.id)
        
        # Then
        assert result is True
        # 삭제 확인
        deleted_memo = memo_repository.get_memo_by_id(db_session, test_memo.id)
        assert deleted_memo is None
    
    def test_delete_memo_not_found(self, db_session: Session):
        """존재하지 않는 메모 삭제 테스트"""
        # When
        result = memo_repository.delete_memo(db_session, 999)
        
        # Then
        assert result is False
