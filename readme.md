### 1. 프로젝트 개요
FastAPI와 PostgreSQL을 활용한 RESTful API 기반 메모장 애플리케이션 백엔드

### 2. 핵심 기능

**2.1 메모 CRUD 기능**
- 메모 생성: 제목과 내용을 포함한 새 메모 작성
- 메모 조회: 전체 메모 목록 조회 및 개별 메모 상세 조회
- 메모 수정: 기존 메모의 제목 또는 내용 수정
- 메모 삭제: 메모 영구 삭제

**2.2 데이터 모델**
- 메모 ID (자동 생성, Primary Key)
- 제목 (필수, 최대 200자)
- 내용 (선택, 최대 5000자)
- 생성 일시 (자동 생성)
- 수정 일시 (자동 업데이트)

**2.3 API 엔드포인트**
- `POST /api/v1/memos` - 메모 생성
- `GET /api/v1/memos` - 메모 목록 조회 (페이징 지원)
- `GET /api/v1/memos/{memo_id}` - 특정 메모 조회
- `PUT /api/v1/memos/{memo_id}` - 메모 수정
- `DELETE /api/v1/memos/{memo_id}` - 메모 삭제


### 3. 기술 요구사항

**3.1 백엔드 프레임워크**
- FastAPI (최신 버전)

**3.2 데이터베이스**
- PostgreSQL 14+
- SQLAlchemy ORM 활용
- Alembic을 통한 마이그레이션 관리

**3.3 테스팅**
- pytest를 활용한 테스트 프레임워크
- 유닛 테스트: 각 레이어별 독립 테스트
- 통합 테스트: API 엔드포인트 E2E 테스트
- 테스트 커버리지 80% 이상 목표

**3.4 개발 환경**
- Python 3.10+
- Poetry 또는 pip를 통한 의존성 관리
- Docker를 활용한 PostgreSQL 로컬 환경 구성