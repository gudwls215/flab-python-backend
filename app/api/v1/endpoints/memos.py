"""
메모 API 엔드포인트
메모 CRUD 기능을 제공하는 REST API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.memo import MemoCreate, MemoUpdate, MemoResponse, MemoListResponse
from app.services.memo_service import memo_service
from app.exceptions.memo_exceptions import MemoNotFoundException


router = APIRouter()


@router.post(
    "",
    response_model=MemoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="메모 생성",
    description="새로운 메모를 생성합니다."
)
def create_memo(
    memo_data: MemoCreate,
    db: Session = Depends(get_db_session)
) -> MemoResponse:
    """
    새로운 메모 생성
    
    - **title**: 메모 제목 (필수, 최대 200자)
    - **content**: 메모 내용 (선택, 최대 5000자)
    """
    return memo_service.create_memo(db, memo_data)


@router.get(
    "",
    response_model=MemoListResponse,
    summary="메모 목록 조회",
    description="메모 목록을 페이징하여 조회합니다."
)
def get_memos(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(100, ge=1, le=1000, description="조회할 최대 레코드 수"),
    db: Session = Depends(get_db_session)
) -> MemoListResponse:
    """
    메모 목록 조회 (페이징)
    
    - **skip**: 건너뛸 레코드 수 (기본값: 0)
    - **limit**: 조회할 최대 레코드 수 (기본값: 100, 최대: 1000)
    """
    return memo_service.get_memos(db, skip, limit)


@router.get(
    "/{memo_id}",
    response_model=MemoResponse,
    summary="메모 조회",
    description="특정 메모를 ID로 조회합니다."
)
def get_memo(
    memo_id: int,
    db: Session = Depends(get_db_session)
) -> MemoResponse:
    """
    특정 메모 조회
    
    - **memo_id**: 조회할 메모 ID
    """
    try:
        return memo_service.get_memo(db, memo_id)
    except MemoNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{memo_id}",
    response_model=MemoResponse,
    summary="메모 수정",
    description="기존 메모를 수정합니다."
)
def update_memo(
    memo_id: int,
    memo_data: MemoUpdate,
    db: Session = Depends(get_db_session)
) -> MemoResponse:
    """
    메모 수정
    
    - **memo_id**: 수정할 메모 ID
    - **title**: 메모 제목 (선택, 최대 200자)
    - **content**: 메모 내용 (선택, 최대 5000자)
    
    제공된 필드만 업데이트됩니다.
    """
    try:
        return memo_service.update_memo(db, memo_id, memo_data)
    except MemoNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{memo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="메모 삭제",
    description="메모를 영구적으로 삭제합니다."
)
def delete_memo(
    memo_id: int,
    db: Session = Depends(get_db_session)
) -> None:
    """
    메모 삭제
    
    - **memo_id**: 삭제할 메모 ID
    """
    try:
        memo_service.delete_memo(db, memo_id)
    except MemoNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
