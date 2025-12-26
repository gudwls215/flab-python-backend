# 메모장 CRUD 백엔드 API

FastAPI와 PostgreSQL을 활용한 RESTful API 기반 메모장 애플리케이션 백엔드

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [테스트](#테스트)
- [개발 가이드](#개발-가이드)

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

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
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

## 🧪 테스트

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

## 💻 개발 가이드

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
