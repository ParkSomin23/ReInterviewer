from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

from app.core.config import settings

"""
이거 보고 도입하기: https://wikidocs.net/295889
"""


class UserCreate(BaseModel):

    email: EmailStr
    name: str = None

    # 삭제
    hashed_password: str


# 2. 로그인 시 받을 데이터
class UserLogin(BaseModel):

    email: EmailStr
    hashed_password: str  # 삭제


# 3. API 응답으로 내보낼 데이터 (비밀번호 절대 제외!)
class UserResponse(BaseModel):

    id: str
    email: EmailStr
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 객체를 자동으로 변환


class UserSearchRequest(BaseModel):

    email: Optional[EmailStr]
    name: Optional[str]
