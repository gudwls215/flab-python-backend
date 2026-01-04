# 메모장 CRUD 백엔드 API

FastAPI와 PostgreSQL을 활용한 RESTful API 기반 메모장 애플리케이션 백엔드

---

## 프로젝트 개요

FastAPI와 PostgreSQL을 활용한 RESTful API 기반 메모장 애플리케이션 백엔드입니다.
- 완전한 CRUD 기능 제공
- 계층화된 아키텍처 (API - Service - Repository - Model)
- 테스트 커버리지 94%
- OpenAPI/Swagger 자동 문서화

## 주요 기능

### 메모 CRUD 기능
- ✅ 메모 생성 (제목 필수, 내용 선택)
- ✅ 메모 목록 조회 (페이징 지원)
- ✅ 특정 메모 조회
- ✅ 메모 수정 (부분 업데이트 지원)
- ✅ 메모 삭제

### 데이터 모델
- 메모 ID (자동 생성, Primary Key)
- 제목 (필수, 최대 200자)
- 내용 (선택, 최대 5000자)
- 생성 일시 (자동 생성)
- 수정 일시 (자동 업데이트)

### API 엔드포인트
- `POST /api/v1/memos` - 메모 생성
- `GET /api/v1/memos` - 메모 목록 조회 (페이징 지원)
- `GET /api/v1/memos/{memo_id}` - 특정 메모 조회
- `PUT /api/v1/memos/{memo_id}` - 메모 수정
- `DELETE /api/v1/memos/{memo_id}` - 메모 삭제

---

## 기술 스택

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0.23
- **Migration**: Alembic 1.12.1
- **Validation**: Pydantic 2.5.0
- **Testing**: pytest 7.4.3, pytest-cov
- **Server**: Uvicorn 0.24.0
- **Language**: Python 3.10+

---

## 설치 및 실행

### 사전 요구사항

- Python 3.10 이상
- Docker Desktop (PostgreSQL 실행용)
- Git

### 1. 저장소 클론 및 이동

```bash
git clone <repository-url>
cd flab-python-backend
```

### 2. uv 설치 (아직 설치하지 않은 경우)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 가상환경 생성 및 의존성 설치

```bash
# uv를 사용하여 가상환경 생성 및 의존성 설치
uv venv
uv pip install -r requirements.txt

# 가상환경 활성화
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# 필요시 .env 파일 수정
```

### 5. PostgreSQL 시작 (Docker)

```bash
docker-compose up -d
```

### 6. 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

### 7. 서버 실행

```bash
# 개발 모드 (자동 재시작)
uvicorn app.main:app --reload

# 또는
python -m app.main
```

서버가 실행되면 다음 주소로 접속 가능합니다:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 테스트

### 전체 테스트 실행

```bash
pytest tests/ -v
```

### 커버리지 포함 테스트

```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
```

**테스트 결과:**
- ✅ 총 42개 테스트 (유닛 23개 + 통합 19개)
- ✅ 테스트 커버리지: **94%**
- ✅ 모든 CRUD 기능 테스트
- ✅ 에러 케이스 테스트

### 유닛 테스트만 실행

```bash
pytest tests/unit/ -v
```

### 통합 테스트만 실행

```bash
pytest tests/integration/ -v
```

---

## 부하 테스트 (Locust)

### Locust 설치

```bash
# uv를 사용하여 설치
uv pip install locust
```

### 부하 테스트 실행

#### 1. CLI 모드 (헤드리스)

```bash
# 기본 부하 테스트 (10명 사용자, 60초간)
locust --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless --html locust_report.html

# 고부하 테스트 (100명 사용자, 5분간)
locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 5m --headless --html locust_report.html
```

#### 2. Web UI 모드

```bash
# Locust 웹 UI 실행
locust --host=http://localhost:8000

# 브라우저에서 http://localhost:8089 접속
```

### 부하 테스트 결과 예시

**테스트 설정:**
- 사용자 수: 10명 (MemoUser 5명 + HeavyLoadUser 5명)
- 증가율: 초당 2명
- 테스트 시간: 60초

**결과:**
- ✅ 총 요청 수: **696건**
- ✅ 평균 RPS: **11.7 req/s**
- ✅ 실패율: **0%**
- ✅ 평균 응답 시간: **77ms**
- ✅ 중앙값 응답 시간: **49ms**
- ✅ 95 백분위수: **97ms**
- ✅ 99 백분위수: **2100ms** (초기 DB 연결 시간 포함)

**엔드포인트별 성능:**
- `POST /api/v1/memos (대량 생성)`: 447건, 평균 77ms
- `GET /api/v1/memos (대량 조회)`: 99건, 평균 40ms
- `GET /api/v1/memos (목록 조회)`: 42건, 평균 14ms
- `GET /api/v1/memos/{id} (상세 조회)`: 28건, 평균 11ms
- `POST /api/v1/memos (생성)`: 26건, 평균 60ms
- `PUT /api/v1/memos/{id} (수정)`: 14건, 평균 61ms
- `DELETE /api/v1/memos/{id} (삭제)`: 9건, 평균 55ms

### 부하 테스트 시나리오

`locustfile.py`에는 두 가지 사용자 시나리오가 포함되어 있습니다:

1. **MemoUser** - 일반 사용자 패턴
   - 메모 목록 조회 (가중치: 3)
   - 메모 상세 조회 (가중치: 2)
   - 메모 생성 (가중치: 2)
   - 메모 수정 (가중치: 1)
   - 메모 삭제 (가중치: 1)

2. **HeavyLoadUser** - 고부하 사용자 패턴
   - 대량 메모 생성 (가중치: 5)
   - 대량 목록 조회 (가중치: 3)

---

## 개발 가이드

### 프로젝트 구조

```
flab-python-backend/
├── app/
│   ├── api/                      # API 엔드포인트
│   │   ├── deps.py              # 의존성 주입
│   │   └── v1/endpoints/        # v1 API 라우터
│   ├── models/                   # SQLAlchemy ORM 모델
│   ├── schemas/                  # Pydantic 스키마
│   ├── repositories/             # 데이터 접근 레이어
│   ├── services/                 # 비즈니스 로직 레이어
│   ├── exceptions/               # 커스텀 예외
│   ├── config.py                # 환경 설정
│   ├── database.py              # DB 연결 설정
│   └── main.py                  # FastAPI 앱 진입점
├── tests/
│   ├── unit/                    # 유닛 테스트
│   ├── integration/             # 통합 테스트
│   └── conftest.py             # pytest 설정
├── alembic/                     # 마이그레이션 파일
├── docker-compose.yml           # PostgreSQL 컨테이너
└── requirements.txt             # 의존성 목록
```

### 코드 스타일

- PEP 8 준수
- Type hints 사용
- Docstring 작성

### 데이터베이스 마이그레이션

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 환경 변수

`.env` 파일에서 다음 변수 설정:

```env
# Database
DATABASE_URL=postgresql://memo_user:memo_password@localhost:5432/memo_db

# Application
APP_NAME=Memo API
APP_VERSION=1.0.0
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 📄 라이선스

이 프로젝트는 개인 학습 목적으로 작성되었습니다.
