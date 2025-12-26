"""
애플리케이션 설정 관리
환경 변수를 통한 설정 로드 및 관리
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # Application Settings
    APP_NAME: str = "Memo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str
    
    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database Connection Pool Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """CORS_ORIGINS를 문자열에서 리스트로 변환"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# 전역 설정 인스턴스
settings = Settings()
