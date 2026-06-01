import uuid
from nanoid import generate

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
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
    questions = relationship(
        "InterviewQuestion", back_populates="interview", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_slug = Column(String(12), ForeignKey("interviews.slug"), index=True)

    interview_question_id = Column(
        Integer, ForeignKey("interview_questions.id"), nullable=True
    )

    role = Column(String(10))  # "user" or "assistant"
    content = Column(Text)
    audio_path = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    interview = relationship("Interview", back_populates="messages")
    interview_question = relationship("InterviewQuestion", back_populates="messages")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    interview_slug = Column(String(12), ForeignKey("interviews.slug"), index=True)

    # Pydantic 필드 매핑
    question_num = Column(
        Integer, nullable=False, index=True
    )  # 질문 순서 (추후 순서 수정을 위한 값)
    question = Column(Text, nullable=False)  # 핵심 질문
    user_answer = Column(Text, nullable=True)  # 사용자 답변
    interviewer_reaction = Column(Text, nullable=True)  # 면접관 반응
    self_evaluation = Column(Text, nullable=True)  # 본인 피드백
    etc = Column(Text, nullable=True)  # 기타 사항

    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 관계 설정
    interview = relationship("Interview", back_populates="questions")
    messages = relationship(
        "Message", back_populates="interview_question", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("id", "question_num", name="uq_survey_question_num"),
    )
