from pathlib import Path
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models import Interview
from app.domains.project.schema import InterviewCreate, InterviewResponse
from app.core.config import settings


def create_user_interview(db: Session, interview_data: InterviewCreate, user_id: str):

    db_interview = Interview(
        **interview_data.model_dump(), user_id=user_id, status="PENDING"
    )

    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # 폴더 생성
    proj_path = Path(settings.proj_path) / db_interview.slug
    if proj_path.exists():
        raise FileExistsError("Interview가 존재합니다. 생성할 수 없습니다.")

    audio_path = proj_path / "audios"
    text_path = proj_path / "texts"

    proj_path.mkdir()
    audio_path.mkdir()
    text_path.mkdir()

    return db_interview


def get_my_interviews(db: Session, user_id: str):
    return db.query(Interview).filter(Interview.user_id == user_id).all()
