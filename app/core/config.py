import os

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    root_path: Path = Path(__file__).resolve().parent.parent.parent
    proj_path: Path = root_path / "projects"

    stt_model: str = "whisper"

    # whisper
    whisper_version: str = "base"
    whisper_cli_path: Path = root_path / "externals/whisper_cpp/build/bin/whisper-cli"

    # IceFall 추후 추가

    # text
    text_path: Path = proj_path / "texts"

    # API 설정
    API_VERSION: str = "0.1.0"


settings = Settings()
