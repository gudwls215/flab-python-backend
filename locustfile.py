"""
Locust 부하 테스트 파일
메모 CRUD API에 대한 부하 테스트 시나리오
"""

from locust import HttpUser, task, between
import random
import json


class MemoUser(HttpUser):
    """메모 API 사용자 시뮬레이션"""
    
    # 요청 간 대기 시간 (1~3초)
    wait_time = between(1, 3)
    
    # 생성된 메모 ID 저장
    memo_ids = []
    
    def on_start(self):
        """테스트 시작 시 초기 메모 생성"""
        # 초기 메모 3개 생성
        for i in range(3):
            response = self.client.post(
                "/api/v1/memos",
                json={
                    "title": f"초기 메모 {i+1}",
                    "content": f"부하 테스트를 위한 초기 메모 내용 {i+1}"
                }
            )
            if response.status_code == 201:
                memo_id = response.json().get("id")
                if memo_id:
                    self.memo_ids.append(memo_id)
    
    @task(3)
    def get_memos_list(self):
        """메모 목록 조회 (가중치: 3)"""
        # 랜덤 페이지 조회
        skip = random.randint(0, 20)
        limit = random.randint(5, 20)
        
        with self.client.get(
            f"/api/v1/memos?skip={skip}&limit={limit}",
            catch_response=True,
            name="/api/v1/memos (목록 조회)"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"목록 조회 실패: {response.status_code}")
    
    @task(2)
    def get_memo_detail(self):
        """특정 메모 조회 (가중치: 2)"""
        if self.memo_ids:
            memo_id = random.choice(self.memo_ids)
            with self.client.get(
                f"/api/v1/memos/{memo_id}",
                catch_response=True,
                name="/api/v1/memos/{id} (상세 조회)"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    # 삭제된 메모일 수 있음
                    self.memo_ids.remove(memo_id)
                    response.success()
                else:
                    response.failure(f"상세 조회 실패: {response.status_code}")
    
    @task(2)
    def create_memo(self):
        """메모 생성 (가중치: 2)"""
        memo_data = {
            "title": f"부하테스트 메모 {random.randint(1, 10000)}",
            "content": f"부하 테스트 중 생성된 메모입니다. {random.randint(1, 10000)}"
        }
        
        with self.client.post(
            "/api/v1/memos",
            json=memo_data,
            catch_response=True,
            name="/api/v1/memos (생성)"
        ) as response:
            if response.status_code == 201:
                memo_id = response.json().get("id")
                if memo_id:
                    self.memo_ids.append(memo_id)
                response.success()
            else:
                response.failure(f"메모 생성 실패: {response.status_code}")
    
    @task(1)
    def update_memo(self):
        """메모 수정 (가중치: 1)"""
        if self.memo_ids:
            memo_id = random.choice(self.memo_ids)
            update_data = {
                "title": f"수정된 메모 {random.randint(1, 10000)}",
                "content": f"부하 테스트 중 수정된 내용 {random.randint(1, 10000)}"
            }
            
            with self.client.put(
                f"/api/v1/memos/{memo_id}",
                json=update_data,
                catch_response=True,
                name="/api/v1/memos/{id} (수정)"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    # 삭제된 메모일 수 있음
                    self.memo_ids.remove(memo_id)
                    response.success()
                else:
                    response.failure(f"메모 수정 실패: {response.status_code}")
    
    @task(1)
    def delete_memo(self):
        """메모 삭제 (가중치: 1)"""
        if len(self.memo_ids) > 3:  # 최소 3개는 유지
            memo_id = random.choice(self.memo_ids)
            
            with self.client.delete(
                f"/api/v1/memos/{memo_id}",
                catch_response=True,
                name="/api/v1/memos/{id} (삭제)"
            ) as response:
                if response.status_code == 204:
                    self.memo_ids.remove(memo_id)
                    response.success()
                elif response.status_code == 404:
                    # 이미 삭제된 메모
                    if memo_id in self.memo_ids:
                        self.memo_ids.remove(memo_id)
                    response.success()
                else:
                    response.failure(f"메모 삭제 실패: {response.status_code}")
    
    @task(1)
    def health_check(self):
        """헬스 체크 (가중치: 1)"""
        with self.client.get(
            "/",
            catch_response=True,
            name="/ (헬스 체크)"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"헬스 체크 실패: {response.status_code}")


class HeavyLoadUser(HttpUser):
    """고부하 시나리오 - 대량의 메모 생성 및 조회"""
    
    wait_time = between(0.5, 1.5)
    memo_ids = []
    
    @task(5)
    def create_multiple_memos(self):
        """연속으로 메모 생성"""
        for _ in range(3):
            response = self.client.post(
                "/api/v1/memos",
                json={
                    "title": f"대량 생성 메모 {random.randint(1, 100000)}",
                    "content": f"대량 테스트 내용 " * 50  # 긴 내용
                },
                name="/api/v1/memos (대량 생성)"
            )
            if response.status_code == 201:
                memo_id = response.json().get("id")
                if memo_id:
                    self.memo_ids.append(memo_id)
    
    @task(3)
    def get_large_list(self):
        """큰 페이지 사이즈로 목록 조회"""
        self.client.get(
            "/api/v1/memos?skip=0&limit=100",
            name="/api/v1/memos (대량 조회)"
        )
