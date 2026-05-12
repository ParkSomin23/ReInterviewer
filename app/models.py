import uuid
from nanoid import generate

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    # 고유 ID (UUID 문자열)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # 사용자 정보
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 실제 비번이 아닌 해시값 저장
    name = Column(String, nullable=True)

    # 메타데이터
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, nullable=True)

    # 관계 설정: 한 사용자는 여러 개의 인터뷰를 가질 수 있음
    # back_populates는 Interview 모델에도 'owner'라는 필드가 있어야 함을 의미합니다.
    interviews = relationship(
        "Interview", back_populates="owner", cascade="all, delete-orphan"
    )


class Interview(Base):
    __tablename__ = "interviews"

    # SQLite는 UUID 타입을 지원하지 않으므로 String으로 저장하고 기본값을 uuid4로 줍니다.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    slug = Column(
        String(12), unique=True, index=True, default=lambda: generate(size=12)
    )

    company_name = Column(String, nullable=False)
    position = Column(String)
    status = Column(String, default="in_progress")

    interview_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

    summary = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)  # 리스트 대신 JSON 형태의 텍스트로 저장

    user_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="interviews")
