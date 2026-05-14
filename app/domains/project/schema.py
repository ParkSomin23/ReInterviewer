from pydantic import BaseModel, Field
from typing import Optional, List

from uuid import UUID
from datetime import datetime, timezone

from app.core.config import settings


class InterviewCreate(BaseModel):

    company_name: str
    position: str
    interview_date: datetime

    model_config = {"from_attributes": True}


class InterviewResponse(BaseModel):

    slug: str

    company_name: str
    position: str

    status: str

    interview_date: datetime
    created_at: datetime

    # 요약이나 액션 아이템은 처음엔 없을 수 있으니 Optional로 추가하면 좋습니다.
    summary: Optional[str] = None
    action_items: Optional[list[str]] = None

    # SQLAlchemy 같은 ORM 객체를 자동으로 Pydantic으로 변환해주기 위한 설정 (Pydantic v2)
    model_config = {"from_attributes": True}
