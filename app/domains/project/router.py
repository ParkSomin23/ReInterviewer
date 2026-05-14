import os
import subprocess
import json

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

import app.domains.project.service as interview_service
from app.domains.project.schema import (
    InterviewCreate,
    InterviewResponse,
)
from app.models import Interview

from app.core.config import settings
from app.core.dependencies import get_current_user_id

from app.database import get_db

# from app.domains.user import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{interview_slug}", response_model=InterviewResponse)
def get_interview_detail(
    interview_slug: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.slug == interview_slug).first()

    # 데이터가 없거나, 주인이 현재 사용자가 아니면 404 혹은 403 에러
    if not interview or interview.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")

    return interview


@router.post("", response_model=InterviewResponse)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):

    return interview_service.create_user_interview(db, interview_data, current_user_id)


@router.delete("/{interview_slug}", status_code=204)
def delete_interview(
    interview_slug: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    interview_service.delete_user_interview(db, interview_slug, current_user_id)

    return None


@router.get("", response_model=list[InterviewResponse])
def get_my_interviews(
    current_user_id: str = Depends(
        get_current_user_id
    ),  # 실제로는 JWT 토큰 등 인증 로직을 통해 가져옵니다.
    db: Session = Depends(get_db),
):

    interviews = db.query(Interview).filter(Interview.user_id == current_user_id).all()

    return interviews
