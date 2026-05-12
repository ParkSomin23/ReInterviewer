import os
import subprocess
import json
import shutil

from datetime import datetime

from pathlib import Path
from typing import Optional
from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    Query,
    Depends,
    UploadFile,
    Body,
    File,
)

from app.domains.audio.service import AudioService
from app.domains.audio.schema import (
    AudioBase,
    AudioProcessRequest,
    AudioProcessResponse,
)

from app.core.config import settings

# from app.core.dependencies import get_config

router = APIRouter(prefix="/audios", tags=["audios"])


def get_audio_service(
    # config=Depends(get_config),
) -> AudioService:
    """BookService 의존성 주입"""

    return AudioService()


@router.get("/infos", response_model=AudioBase)
def get_audio_info(request: AudioBase) -> AudioBase:

    file_path = "/Users/somin/Desktop/github/ReInterviewer/externals/whisper_cpp/samples/jfk.wav"

    # ffprobe에서 JSON 형태로 재생 시간 정보만 뽑아오기
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        file_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    print(data)  # f"재생 시간: {duration}초")


@router.post("/uploaded", response_model=AudioProcessResponse)
def stt_uploaded_audios(
    audio_request: AudioProcessRequest,
    service: AudioService = Depends(get_audio_service),
) -> AudioProcessResponse:

    response = service.preprocess_audio(audio_request)

    return response


@router.post("/recorded", response_model=AudioProcessResponse)
def stt_recorded_audios(
    file: UploadFile,
    ori_audio_path: str = Form(...),
    service: AudioService = Depends(get_audio_service),
) -> AudioProcessResponse:

    audio_path = Path(ori_audio_path)
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    # 파일 저장
    try:
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            buffer.flush()
            os.fsync(buffer.fileno())
    finally:
        file.file.close()

    request_data = AudioProcessRequest(ori_audio_path=audio_path)
    response = service.preprocess_audio(request_data)
    return response
