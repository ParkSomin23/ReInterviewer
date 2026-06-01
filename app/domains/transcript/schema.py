from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Tuple, Annotated, ClassVar
from pathlib import Path

from app.core.config import settings

PROJ_PATH = settings.PROJ_PATH


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
    # Optional로 타입을 명시하고, json_schema_extra 대신 v2 전용 examples 필드를 사용합니다.
    status: Optional[str] = Field(default=None, examples=["success", "fail"])

    audio_file: Optional[Path] = Field(
        default=None,
        title="입력된 오디오 파일 이름",
        examples=["3284ner21314_resampled.wav"],
    )

    texts: Optional[List[str]] = Field(
        default=None,
        title="오디오 전사 내용",
        # 리스트 자체의 예시이므로 이 형태가 올바릅니다.
        examples=[["오디오 내용을 텍스트로 내보냅니다.", "다음 문장입니다."]],
    )

    timestamps: Optional[List[Tuple[float, float]]] = Field(
        default=None,
        title="timestamps",
        description="각 text 시작과 끝 초(s)를 저장합니다.",
        # 튜플() 대신 JSON 표준인 배열[ ] 구조로 예시를 작성해야 에러가 안 납니다!
        examples=[[[1.03, 2.07], [3.013, 4.92]]],
    )

    speakers: Optional[List[int]] = Field(
        default=None,
        title="다화자 id 저장",
        description="오디오에서 말하는 화자 확인",
        examples=[[0, 1, 0]],
    )


class MessageRequest(BaseModel):

    interview_slug: str

    role: str = Field(
        ...,
        title="chatting role",
        description="message role",
        examples=["user", "assistant"],
    )

    content: str = Field(
        ...,
        title="content",
        description="message text",
    )

    audio_path: Optional[str] = Field(
        default=None,
        title="오디오 경로",
        description="녹음 혹은 오디오 업로드된 파일 경로",
    )


class MessageResponse(BaseModel):

    id: int
    interview_slug: str

    role: str = Field(
        ...,
        title="chatting role",
        description="message role",
        examples=["user", "assistant"],
    )

    content: str = Field(
        ...,
        title="content",
        description="message text",
    )

    audio_path: Optional[str] = Field(
        default=None,
        title="오디오 경로",
        description="녹음 혹은 오디오 업로드된 파일 경로",
    )
    created_at: datetime = Field(
        title="메시지 생성된 시간", description="해당 메시지가 생성된 시간"
    )
    modified_at: datetime = Field(
        title="메시지 수정 시간", description="해당 메시지가 수정된 시간"
    )

    class Config:
        from_attributes = True
