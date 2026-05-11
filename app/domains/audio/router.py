import os
import subprocess
import json

from fastapi import APIRouter, HTTPException, Query, Depends

from app.domains.audio.service import AudioService
from app.domains.audio.schema import AudioBase, AudioProcessRequest, AudioProcessResponse

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
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", file_path]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    duration = data["format"]["duration"]
    print(f"재생 시간: {duration}초")


@router.get("/preprocess", response_model=AudioProcessResponse)
def preprocess_audio_for_stt(
    audio_path: str, service: AudioService = Depends(get_audio_service)
) -> AudioProcessResponse:

    response = service.preprocess_audio(AudioProcessRequest(ori_audio_path=audio_path))

    return response
