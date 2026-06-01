import streamlit as st

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 1. DB 파일 경로 설정
# sqlite:/// 뒤의 ./는 현재 위치를 의미하며 interview_app.db라는 파일이 생성됩니다.
SQLALCHEMY_DATABASE_URL = settings.DB_URL


# 2. 엔진 생성
# check_same_thread=False는 SQLite를 FastAPI(멀티 쓰레드)에서 쓸 때 필수 설정입니다.
@st.cache_resource
def get_db_engine():
    return create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
    )


engine = get_db_engine()

# 3. 세션 설정 (DB 연결을 관리하는 객체)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델(테이블)을 만들 때 상속받을 기본 클래스
Base = declarative_base()


# 5. DB 세션을 가져오는 의존성 함수 (FastAPI 엔드포인트에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
