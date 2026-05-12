from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Annotated, Tuple

from app.domains.audio.schema import (
    AudioBase,
    AudioProcessRequest,
    AudioProcessResponse,
)

import os
import subprocess


class AudioService:

    def __init__(
        self,
    ):

        self.hello = None

    def preprocess_audio(self, request: AudioProcessRequest) -> AudioProcessResponse:

        if not os.path.isfile(request.ori_audio_path):
            raise FileNotFoundError(f"""file doesn't exist, {request.ori_audio_path}""")

        ext = os.path.splitext(request.ori_audio_path)[1]

        resampled_audio_path = str(request.ori_audio_path).replace(
            ext, "_resampled" + ext
        )
        if os.path.isfile(resampled_audio_path):
            return AudioProcessResponse(
                status="success", resampled_audio_path=resampled_audio_path
            )

        # 1. Denosing

        # 2. VAD

        # 3. Speaker Diarization

        # 4. Resample audio to ensure compatibility with the STT model
        command = [
            "ffmpeg",
            "-loglevel",
            "error",
            "-y",
            "-i",
            request.ori_audio_path,
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            resampled_audio_path,
        ]
        subprocess.run(command, check=True)

        return AudioProcessResponse(
            status="success", resampled_audio_path=resampled_audio_path
        )

    # def resample_audio(self, request: AudioProcessRequest):

    #     # check if audio is already resampled
    #     if request.resampled_audio_path is not None:
    #         resampled_audio_path = os.path.join(settings.proj_path, request.resampled_audio_path)
    #         subprocess.Popen(f"""ffmpeg -i {resampled_audio_path} 2>&1 | grep -A1 Duration:""")

    #     ori_audio_path = os.path.join(settings.proj_path, request.ori_audio_path)

    #     if not os.path.isfile(ori_audio_path):
    #         raise FileNotFoundError(f"""Cannot find file: {ori_audio_path}""")
