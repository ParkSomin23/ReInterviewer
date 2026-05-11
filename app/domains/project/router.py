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


@router.post("/create", response_model=InterviewResponse)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):

    return interview_service.create_user_interview(db, interview_data, current_user_id)


@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
def get_interview_detail(
    interview_id: str, current_user_id: str, db: Session = Depends(get_db)
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    # 데이터가 없거나, 주인이 현재 사용자가 아니면 404 혹은 403 에러
    if not interview or interview.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")

    return interview


@router.get("/interviews", response_model=list[InterviewResponse])
def get_my_interviews(
    current_user_id: str,  # 실제로는 JWT 토큰 등 인증 로직을 통해 가져옵니다.
    db: Session = Depends(get_db),
):

    # 핵심: .filter를 통해 본인의 user_id와 일치하는 것만 가져옴
    interviews = db.query(Interview).filter(Interview.user_id == current_user_id).all()

    return interviews


@router.post("/create", response_model=InterviewResponse)
def create_interview(
    request: InterviewCreate, db: Session = Depends(get_db)
) -> InterviewResponse:

    db_interview = Interview(
        company_name=request.company_name,
        position=request.position,
        interview_date=request.interview_date,
    )

    # 2. DB에 저장
    db.add(db_interview)
    db.commit()  # 확정
    db.refresh(db_interview)  # 저장 후 생성된 ID 등을 다시 가져오기

    return db_interview
