from enum import Enum
from fastapi import HTTPException


class ErrorCode(Enum):
    # Bad Request
    INVALID_INPUT = 1100

    # Unauthorized
    EMPTY_TOKEN = 2001
    TOKEN_EXPIRED = 2002
    INVALID_TOKEN = 2003
    DENIED_PERMISSION = 2004

    # Not Found
    RESOURCE_NOT_FOUND = 4001

    # Internal Server Error
    UNEXPECTED_ERROR = 9000
    CONNECTION_ERROR = 9001
    MODEL_TIMEOUT = 9101


class OperatedException(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCode, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.code = error_code
