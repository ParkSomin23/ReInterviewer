import uuid
from nanoid import generate

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
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

    # 관계 설정
    interviews = relationship(
        "Interview", back_populates="owner", cascade="all, delete-orphan"
    )


class Interview(Base):
    __tablename__ = "interviews"

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

    messages = relationship(
        "Message", back_populates="interview", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_slug = Column(String(12), ForeignKey("interviews.slug"), index=True)

    role = Column(String(10))  # "user" or "assistant"

    content = Column(Text)
    audio_path = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    interview = relationship("Interview", back_populates="messages")
