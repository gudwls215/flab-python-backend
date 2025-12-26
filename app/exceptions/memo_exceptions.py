"""
메모 관련 커스텀 예외
"""


class MemoNotFoundException(Exception):
    """메모를 찾을 수 없을 때 발생하는 예외"""
    
    def __init__(self, memo_id: int):
        self.memo_id = memo_id
        super().__init__(f"Memo with id {memo_id} not found")


class MemoValidationException(Exception):
    """메모 데이터 검증 실패 시 발생하는 예외"""
    
    def __init__(self, message: str):
        super().__init__(message)
