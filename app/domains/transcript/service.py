import os
import json
import subprocess

from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Annotated, Tuple

from app.domains.transcript.schema import STTRequest, STTResponse
from app.core.config import settings


class STTService:

    def __init__(
        self,
    ):

        self.root_path = settings.root_path
        self.proj_path = settings.proj_path

        self.stt_model = settings.stt_model
        if self.stt_model == "whisper":
            self.model_name = settings.whisper_version
            self.model_path = self.root_path / f"""externals/whisper_cpp/models/ggml-{self.model_name}.bin"""

            self.external_path = settings.whisper_cli_path

    def stt(self, request: STTRequest):

        if not request.resampled_audio_path.is_file():
            return STTResponse(status="fail")

        parent_dir = request.resampled_audio_path.parent
        text_path = parent_dir.parent / "texts"
        text_path.mkdir(parents=True, exist_ok=True)

        # Check if STT result file exists
        output_json_name = text_path / request.resampled_audio_path.stem
        if output_json_name.with_suffix(".json").exists():
            texts, timestamps, speakers = self.json_to_response(output_json_name.with_suffix(".json"))

            return STTResponse(status="success", texts=texts, timestamps=timestamps, speakers=speakers)

        # see "externals/whisper_cpp/examples/cli/README.md" for more options
        command = [
            self.external_path,
            "-m",
            self.model_path,
            "-f",
            request.resampled_audio_path,
            "-l",
            "auto",  # language
            "-oj",  # make json output file
            "-of",
            output_json_name,  # output name
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and error (if any)
        _, error = process.communicate()

        if process.returncode != 0:
            raise Exception(f"""Error processing audio: {error.decode('utf-8')}""")

        if self.stt_model == "whisper":
            texts, timestamps, speakers = self.json_to_response(output_json_name.with_suffix(".json"))
        else:
            raise NotImplementedError(f"{self.stt_model} is not impletmented")

        return STTResponse(status="success", texts=texts, timestamps=timestamps, speakers=speakers)

    def json_to_response(self, json_path):
        """
        Convert Whisper output to STTResponse-compatible format
        """

        if not json_path.exists():
            raise FileNotFoundError(f"""STT Result JSON file not found: {json_path}""")

        with open(json_path, "r", encoding="utf-8") as f:
            stt_json = json.load(f)

        results = stt_json["transcription"]

        texts = []
        timestamps = []
        speakers = []

        for r in results:
            texts.append(r["text"].strip())

            # Normalize time units to seconds
            s = r["offsets"]["from"] / 1000
            e = r["offsets"]["to"] / 1000
            timestamps.append((s, e))

            # TODO: Not Implemented
            speakers.append(-1)

        return texts, timestamps, speakers
