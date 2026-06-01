import shutil
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
    proj_path = Path(settings.PROJ_PATH) / db_interview.slug
    if proj_path.exists():
        raise FileExistsError("Interview가 존재합니다. 생성할 수 없습니다.")

    audio_path = proj_path / "audios"
    text_path = proj_path / "texts"

    proj_path.mkdir()
    audio_path.mkdir()
    text_path.mkdir()

    return db_interview


# TODO: 나중에 정보 수정하기 넣기
# def edit_user_interview(db: Session, interview_data: InterviewCreate, user_id: str):

#     db_interview = (
#         db.query(Interview)
#         .filter(
#             Interview.slug == interview_data["slug"],
#             Interview.user_id == user_id,  # 본인 소유인지 확인
#         )
#         .first()
#     )

#     return db_interview


def delete_user_interview(db: Session, interview_slug: str, user_id: str):

    db_interview = (
        db.query(Interview)
        .filter(
            Interview.slug == interview_slug,
            Interview.user_id == user_id,  # 본인 소유인지 확인
        )
        .first()
    )
    proj_path = Path(settings.PROJ_PATH) / db_interview.slug

    if not db_interview:
        raise HTTPException(
            status_code=404, detail=f"Interview not found: {interview_slug}"
        )

    db.delete(db_interview)
    db.commit()

    # 폴더 삭제
    if proj_path.exists():
        shutil.rmtree(proj_path)


def get_my_interviews(db: Session, user_id: str):
    return db.query(Interview).filter(Interview.user_id == user_id).all()
