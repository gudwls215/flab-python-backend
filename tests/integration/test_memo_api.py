"""
메모 API 통합 테스트
API 엔드포인트 E2E 테스트
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.memo import Memo


class TestMemoAPI:
    """메모 API 통합 테스트"""
    
    def test_create_memo_success(self, client: TestClient):
        """메모 생성 성공 테스트"""
        # Given
        memo_data = {
            "title": "새로운 메모",
            "content": "새로운 메모 내용"
        }
        
        # When
        response = client.post("/api/v1/memos", json=memo_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == memo_data["title"]
        assert data["content"] == memo_data["content"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_memo_without_content(self, client: TestClient):
        """내용 없이 메모 생성 테스트"""
        # Given
        memo_data = {
            "title": "제목만 있는 메모"
        }
        
        # When
        response = client.post("/api/v1/memos", json=memo_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == memo_data["title"]
        assert data["content"] is None
    
    def test_create_memo_without_title_fails(self, client: TestClient):
        """제목 없이 메모 생성 시 실패 (422)"""
        # Given
        memo_data = {
            "content": "내용만 있음"
        }
        
        # When
        response = client.post("/api/v1/memos", json=memo_data)
        
        # Then
        assert response.status_code == 422
    
    def test_create_memo_with_empty_title_fails(self, client: TestClient):
        """빈 제목으로 메모 생성 시 실패 (422)"""
        # Given
        memo_data = {
            "title": "",
            "content": "내용"
        }
        
        # When
        response = client.post("/api/v1/memos", json=memo_data)
        
        # Then
        assert response.status_code == 422
    
    def test_create_memo_with_long_title_fails(self, client: TestClient):
        """최대 길이 초과 제목으로 메모 생성 시 실패 (422)"""
        # Given
        memo_data = {
            "title": "a" * 201,
            "content": "내용"
        }
        
        # When
        response = client.post("/api/v1/memos", json=memo_data)
        
        # Then
        assert response.status_code == 422
    
    def test_get_memos_empty(self, client: TestClient):
        """빈 메모 목록 조회 테스트"""
        # When
        response = client.get("/api/v1/memos")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["skip"] == 0
        assert data["limit"] == 100
    
    def test_get_memos(self, client: TestClient, create_test_memo):
        """메모 목록 조회 테스트"""
        # Given
        create_test_memo(title="메모 1", content="내용 1")
        create_test_memo(title="메모 2", content="내용 2")
        create_test_memo(title="메모 3", content="내용 3")
        
        # When
        response = client.get("/api/v1/memos")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
    
    def test_get_memos_with_pagination(self, client: TestClient, create_test_memo):
        """페이징을 사용한 메모 목록 조회 테스트"""
        # Given
        for i in range(5):
            create_test_memo(title=f"메모 {i+1}", content=f"내용 {i+1}")
        
        # When
        response = client.get("/api/v1/memos?skip=2&limit=2")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["skip"] == 2
        assert data["limit"] == 2
    
    def test_get_memo_by_id_success(self, client: TestClient, create_test_memo):
        """특정 메모 조회 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="조회할 메모", content="조회할 내용")
        
        # When
        response = client.get(f"/api/v1/memos/{test_memo.id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_memo.id
        assert data["title"] == test_memo.title
        assert data["content"] == test_memo.content
    
    def test_get_memo_by_id_not_found(self, client: TestClient):
        """존재하지 않는 메모 조회 시 실패 (404)"""
        # When
        response = client.get("/api/v1/memos/999")
        
        # Then
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_update_memo_success(self, client: TestClient, create_test_memo):
        """메모 수정 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = {
            "title": "수정된 제목",
            "content": "수정된 내용"
        }
        
        # When
        response = client.put(f"/api/v1/memos/{test_memo.id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_memo.id
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
    
    def test_update_memo_partial(self, client: TestClient, create_test_memo):
        """메모 부분 수정 테스트 (제목만)"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = {
            "title": "수정된 제목"
        }
        
        # When
        response = client.put(f"/api/v1/memos/{test_memo.id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == "원본 내용"  # 내용은 그대로
    
    def test_update_memo_not_found(self, client: TestClient):
        """존재하지 않는 메모 수정 시 실패 (404)"""
        # Given
        update_data = {
            "title": "수정된 제목"
        }
        
        # When
        response = client.put("/api/v1/memos/999", json=update_data)
        
        # Then
        assert response.status_code == 404
    
    def test_update_memo_with_empty_title_fails(self, client: TestClient, create_test_memo):
        """빈 제목으로 메모 수정 시 실패 (422)"""
        # Given
        test_memo = create_test_memo(title="원본 제목", content="원본 내용")
        update_data = {
            "title": ""
        }
        
        # When
        response = client.put(f"/api/v1/memos/{test_memo.id}", json=update_data)
        
        # Then
        assert response.status_code == 422
    
    def test_delete_memo_success(self, client: TestClient, create_test_memo):
        """메모 삭제 성공 테스트"""
        # Given
        test_memo = create_test_memo(title="삭제할 메모", content="삭제할 내용")
        
        # When
        response = client.delete(f"/api/v1/memos/{test_memo.id}")
        
        # Then
        assert response.status_code == 204
        
        # 삭제 확인
        get_response = client.get(f"/api/v1/memos/{test_memo.id}")
        assert get_response.status_code == 404
    
    def test_delete_memo_not_found(self, client: TestClient):
        """존재하지 않는 메모 삭제 시 실패 (404)"""
        # When
        response = client.delete("/api/v1/memos/999")
        
        # Then
        assert response.status_code == 404
    
    def test_health_check(self, client: TestClient):
        """Health check 엔드포인트 테스트"""
        # When
        response = client.get("/health")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self, client: TestClient):
        """Root 엔드포인트 테스트"""
        # When
        response = client.get("/")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "app_name" in data
        assert "version" in data
    
    def test_full_crud_workflow(self, client: TestClient):
        """전체 CRUD 워크플로우 테스트"""
        # 1. 메모 생성
        create_data = {"title": "워크플로우 테스트", "content": "테스트 내용"}
        create_response = client.post("/api/v1/memos", json=create_data)
        assert create_response.status_code == 201
        memo_id = create_response.json()["id"]
        
        # 2. 메모 조회
        get_response = client.get(f"/api/v1/memos/{memo_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == create_data["title"]
        
        # 3. 메모 수정
        update_data = {"title": "수정된 제목"}
        update_response = client.put(f"/api/v1/memos/{memo_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["title"] == update_data["title"]
        
        # 4. 메모 목록에서 확인
        list_response = client.get("/api/v1/memos")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 1
        
        # 5. 메모 삭제
        delete_response = client.delete(f"/api/v1/memos/{memo_id}")
        assert delete_response.status_code == 204
        
        # 6. 삭제 확인
        final_get_response = client.get(f"/api/v1/memos/{memo_id}")
        assert final_get_response.status_code == 404
