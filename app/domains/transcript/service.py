
import os
import subprocess

from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Annotated, Tuple

from app.domains.transcript.schema import STTRequest, STTResponse
from app.core.config import settings

class STTService:

    def __init__(self,):

        self.root_path = settings.root_path
        self.proj_path = settings.proj_path

        self.stt_model = settings.stt_model
        if self.stt_model == "whisper":
            self.model_name = settings.whisper_version
            self.model_path = self.root_path / f"""externals/whisper_cpp/models/ggml-{self.model_name}.bin"""
    
            self.external_path = settings.whisper_cli_path

        
    def stt(self, request: STTRequest):

        if not request.resampled_audio_path.is_file():
            return  STTResponse(status="fail")
        
        parent_dir = request.resampled_audio_path.parent
        text_path = parent_dir.parent / "texts"
        text_path.mkdir(parents=True, exist_ok=True)
        
        output_json_name = text_path / request.resampled_audio_path.stem
        if os.path.isfile(str(output_json_name)+".json"):
            return STTResponse(status="success")
        
        # see "externals/whisper_cpp/examples/cli/README.md" for more options
        command = [
            self.external_path,
            "-m", self.model_path,
            "-f", request.resampled_audio_path,
            "-l", "auto", # language
            "-oj", #json 파일로 출력
            "-of", output_json_name #output name
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and error (if any)
        output, error = process.communicate()

        if process.returncode != 0:
            raise Exception(f"""Error processing audio: {error.decode('utf-8')}""")
    
        # # Process and return the output string
        # decoded_str = output.decode('utf-8').strip()
        # processed_str = decoded_str.replace('[BLANK_AUDIO]', '').strip()
        print(output.decode('utf-8'))


        return STTResponse(status="success")