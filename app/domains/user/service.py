from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi import HTTPException, status

from app.database import get_db
from app.models import User

from app.domains.user.schema import UserCreate, UserLogin, UserResponse


# TODO: auth 등으로 확장
def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        # 이미 유저가 있다면 400 에러를 던지고 종료
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다."
        )

    db_user = User(**user_data.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def find_user(db: Session, email: str):

    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"등록된 이메일이 없습니다: {email}"
        )

    return user
