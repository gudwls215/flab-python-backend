"""
데이터베이스 연결 테스트 스크립트
PostgreSQL 연결 확인 및 간단한 쿼리 실행
"""
from sqlalchemy import text
from app.database import engine
from app.config import settings


def test_database_connection():
    """데이터베이스 연결 테스트"""
    print(f"데이터베이스 연결 테스트 시작...")
    print(f"Database URL: {settings.DATABASE_URL}")
    print("-" * 50)
    
    try:
        # 데이터베이스 연결 테스트
        with engine.connect() as connection:
            # PostgreSQL 버전 확인
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ 데이터베이스 연결 성공!")
            print(f"PostgreSQL 버전: {version[:50]}...")
            print()
            
            # 현재 데이터베이스 확인
            result = connection.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"현재 데이터베이스: {db_name}")
            
            # 현재 사용자 확인
            result = connection.execute(text("SELECT current_user"))
            user = result.fetchone()[0]
            print(f"현재 사용자: {user}")
            
            print()
            print("-" * 50)
            print("✓ 모든 데이터베이스 연결 테스트 통과!")
            return True
            
    except Exception as e:
        print(f"✗ 데이터베이스 연결 실패!")
        print(f"에러: {e}")
        print()
        print("Docker 컨테이너가 실행 중인지 확인하세요:")
        print("  docker-compose up -d")
        return False


if __name__ == "__main__":
    test_database_connection()
