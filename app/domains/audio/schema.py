import os

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Annotated, ClassVar
from pathlib import Path

from app.core.config import settings

PROJ_PATH = settings.proj_path


class AudioBase(BaseModel):

    ori_audio_path: Path = Field(
        ...,
        title="입력 받은 오디오 경로",
        description="원본 오디오 파일의 경로입니다. 절대 경로를 직접 입력하거나, \
            프로젝트 번호로 시작하는 상대 경로(예: 0000/...)를 입력할 수 있습니다. \
            상대 경로 입력 시 서버의 프로젝트 루트 경로와 자동으로 병합됩니다.",
        json_schema_extra={
            "examples": [
                "0000/audios/tmp_0001.wav",
                "/Users/AAA/Desktop/ReInterviewer/projects/0000/audios/tmp_0001.wav",
            ]
        },
    )

    ori_audio_sr: int = Field(..., title="입력 받은 오디오 sampling rate")
    ori_audio_bitrate: int = Field(..., title="입력 받은 오디오 bit rate")

    resampled_audio_path: Path = Field(
        ...,
        title="리샘플링된 오디오 파일 경로입니다. ",
        json_schema_extra={"examples": ["0000/resampled_audios/tmp_0001.wav"]},
    )

    @field_validator("ori_audio_path", "resampled_audio_path")
    @classmethod
    def join_with_base_path(cls, v: str) -> Path:

        PROJ_PATH = settings.proj_path
        if os.path.isabs(v):
            return v

        return os.path.join(PROJ_PATH, v)

    def get_proj_id(self) -> str:

        proj_id = self.ori_audio_path.split(os.sep)[-3]

        return proj_id


class AudioProcessRequest(BaseModel):

    ori_audio_path: Path = Field(
        ...,
        title="입력 받은 오디오 경로",
        description="원본 오디오 파일의 경로입니다. 절대 경로를 직접 입력하거나, \
            프로젝트 번호로 시작하는 상대 경로(예: 0000/...)를 입력할 수 있습니다. \
            상대 경로 입력 시 서버의 프로젝트 루트 경로와 자동으로 병합됩니다.",
        json_schema_extra={
            "examples": [
                "0000/audios/tmp_0001.wav",
                "/Users/AAA/Desktop/ReInterviewer/projects/0000/audios/tmp_0001.wav",
            ]
        },
    )
    # target_sr: int = 16000
    # target_bitrate: int = 16

    @field_validator("ori_audio_path")
    @classmethod
    def join_with_base_path(cls, v: Path) -> Path:
        if v.is_absolute():
            return v
        return PROJ_PATH / v


class AudioProcessResponse(BaseModel):

    status: str = Field(None, json_schema_extra={"examples": ["success", "fail"]})
    resampled_audio_path: str = Field(
        ...,
        title="입력 받은 오디오 경로",
        description="reample된 오디오 파일의 경로입니다. 절대 경로를 받아옵니다.",
        json_schema_extra={
            "examples": [
                "/Users/AAA/Desktop/ReInterviewer/projects/0000/audios/tmp_0001_resampled.wav"
            ]
        },
    )


# subprocess.run("ffprobe /Users/somin/Desktop/github/ReInterviewer/externals/whisper_cpp/samples/jfk.wav 2>&1 | grep -A1 Duration:")

# import subprocess

# command =
# result=subprocess.run(command, shell=True, capture_output=True, text=True)
# try:
#     # shell=True를 넣어야 | (파이프)와 2>&1 이 작동합니다.
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)

#     if result.returncode == 0:
#         print("--- 추출 결과 ---")
#         print(result.stdout)
#     else:
#         print("에러 발생:", result.stderr)

# except Exception as e:
#     print(f"실행 중 예외 발생: {e}")
