from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models

from app.core.config import settings
import app.core.health_router as health_router
from app.domains.audio import router as audio_router
from app.domains.transcript import router as transcript_router
from app.domains.user import router as user_router
from app.domains.project import router as proj_router
from app.domains.llm import router as llm_router

import uvicorn
import logging

import sys
import os

# 프로젝트 루트 경로를 찾아서 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..")
sys.path.append(root_dir)

# from externals.whisper_cpp import whisper_processor

# try:
#     result = whisper_processor.process_audio("./audio/wake_word_detected16k.wav", "small")
#     print(result)
# except Exception as e:
#     print(f"Error: {e}")

# # 로깅 설정
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(),  # 콘솔에 출력
#     ],
# )

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8501",
#     "http://127.0.0.1:8501",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 라우터 등록
app.include_router(health_router.router)
app.include_router(audio_router.router)
app.include_router(transcript_router.router)
app.include_router(user_router.router)
app.include_router(proj_router.router)
app.include_router(llm_router.router)


@app.get("/")
def root():
    return {
        "message": "ReInterviewer API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "message": "ReInterviewer API 서버가 작동 중입니다",
    }


if __name__ == "__main__":
    uvicorn.run(app=app)
