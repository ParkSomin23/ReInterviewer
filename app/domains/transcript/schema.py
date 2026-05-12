import os

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Tuple, Annotated, ClassVar
from pathlib import Path

from app.core.config import settings

PROJ_PATH = settings.proj_path


class STTRequest(BaseModel):

    resampled_audio_path: Path = Field(
        ...,
        title="리샘플링된 오디오 파일 경로입니다. ",
        json_schema_extra={"examples": ["0000/resampled_audios/tmp_0001.wav"]},
    )

    @field_validator("resampled_audio_path")
    @classmethod
    def join_with_base_path(cls, v: Path) -> Path:
        if v.is_absolute():
            return v
        return PROJ_PATH / v


class STTResponse(BaseModel):

    status: str = Field(None, json_schema_extra={"examples": ["success", "fail"]})

    texts: List[str] = Field(
        None,
        title="오디오 전사 내용",
        json_schema_extra={
            "examples": ["오디오 내용을 텍스트롤 내보냅니다.", "다음 문장입니다."]
        },
    )

    timestamps: List[Tuple[float, float]] = Field(
        None,
        title="timestamps",
        description="각 text 시작과 끝 초(s)를 저장합니다.",
        examples=[(1.03, 2.07), (3.013, 4.92)],
    )

    speakers: List[int] = Field(
        None, title="다화자 id 저장", description="오디오에서 말하는 화자 확인"
    )
