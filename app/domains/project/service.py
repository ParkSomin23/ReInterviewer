from sqlalchemy.orm import Session
from app import models
from app.domains.project.schema import InterviewCreate, InterviewResponse


def create_user_interview(db: Session, interview_data: InterviewCreate, user_id: str):

    db_interview = models.Interview(
        **interview_data.model_dump(), user_id=user_id, status="PENDING"
    )

    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    return db_interview


def get_my_interviews(db: Session, user_id: str):
    return db.query(models.Interview).filter(models.Interview.user_id == user_id).all()
