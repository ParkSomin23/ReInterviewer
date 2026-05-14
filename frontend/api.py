import io
import requests
import streamlit as st
from nanoid import generate

from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.domains.transcript.schema import MessageRequest, MessageResponse
from app.domains.project.schema import InterviewResponse, InterviewCreate
from app.domains.transcript.schema import STTRequest, STTResponse

API_BASE_URL = "http://localhost:8000"
PROJ_PATH = settings.proj_path


# =========== INTERVIEWS ===========
def get_interview(interview_slug_id: str) -> InterviewResponse:

    try:
        response = requests.get(f"{API_BASE_URL}/projects/{interview_slug_id}")
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"프로젝트 불러오는 중 문제가 발생했습니다: {e}")
        raise ValueError(
            f"인터뷰 프로젝트를 불러오는데 문제가 발생했습니다: project interview_slug_id-{interview_slug_id}\n{e}"
        )


def create_interview(interview_info: InterviewCreate):

    try:
        json_data = interview_info.model_dump(mode="json")

        response = requests.post(f"{API_BASE_URL}/projects", json=json_data)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"프로젝트 생성 중 문제가 발생했습니다: {e}")
        raise ValueError(f"인터뷰 프로젝트를 생성하는 중 문제가 발생했습니다: {e}")


def delete_interview(interview_slug_id: str):

    try:

        response = requests.delete(f"{API_BASE_URL}/projects/{interview_slug_id}")
        response.raise_for_status()

        if response.status_code == 204:
            return True

        return response.json() if response.text else True

    except Exception as e:
        st.error(f"인터뷰 삭제 중 문제가 발생했습니다: {e}")
        raise ValueError(f"인터뷰 삭제 중 문제가 발생했습니다: {e}")


# =========== MESSAGES ===========
def create_msg(interview_slug_id: str, msg: dict) -> MessageResponse:

    try:
        if msg["audio_file"]:
            audio_path = str(
                Path(PROJ_PATH) / interview_slug_id / "audios" / msg["audio_file"]
            )
        else:
            audio_path = None

        payload = MessageRequest(
            interview_slug=interview_slug_id,
            role=msg["role"],
            content=msg["content"],
            audio_path=audio_path,
        )

        response = requests.post(
            f"{API_BASE_URL}/transcripts",
            json=payload.model_dump(),
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"채팅 메시지를 저장하는 중 문제가 발생했습니다: {e}")
        raise ValueError(
            f"""채팅 메시지를 저장하는 중 문제가 발생했습니다: project interview_slug_id-{interview_slug_id}\n{msg['content']}\n{e}"""
        )


def edit_msg(message_id: int, msg: dict) -> MessageResponse:

    try:
        payload = MessageRequest(
            interview_slug=msg["interview_slug"],
            role=msg["role"],
            content=msg["content"],
            audio_path=msg["audio_path"],
        )

        response = requests.patch(
            f"{API_BASE_URL}/transcripts/{message_id}",
            json=payload.model_dump(),
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"채팅 메시지를 수정하는 중 문제가 발생했습니다: {e}")
        raise ValueError(f"""채팅 메시지를 수정하는 중 문제가 발생했습니다: /
            project interview_slug_id-{message_id}\n /
            {msg['content']}\n{e}""")


@st.cache_data
def get_all_msg(interview_slug_id: str):

    try:
        response = requests.get(
            f"{API_BASE_URL}/transcripts/{interview_slug_id}",
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"채팅 메시지를 받아오는 중 문제가 발생했습니다: {e}")
        raise ValueError(f"""채팅 메시지를 받아오는 중 문제가 발생했습니다: /
            project interview_slug_id-{interview_slug_id}\n{e}""")


def delete_msg(message_id: int) -> MessageResponse:

    try:
        response = requests.delete(f"{API_BASE_URL}/transcripts/{message_id}")
        response.raise_for_status()

        if response.status_code == 204:
            return True

        return response.json() if response.text else True

    except Exception as e:
        st.error(f"채팅 메시지를 삭제하는 중 문제가 발생했습니다: {e}")
        raise ValueError(
            f"""채팅 메시지를 삭제하는 중 문제가 발생했습니다: message_id-{message_id}\n{e}"""
        )


# =========== AUDIO & STT ===========
def preprocess_audio(
    interview_slug_id: str, audio_byte: Optional[bytes] = None
) -> STTRequest:

    try:
        audio_name = generate(size=15) + ".wav"
        audio_path = (
            Path(settings.proj_path) / interview_slug_id / "audios" / audio_name
        )

        if audio_byte:
            files = {"file": (audio_name, io.BytesIO(audio_byte), "audio/wav")}
            data = {
                "ori_audio_path": str(audio_path),
            }

            response = requests.post(
                f"{API_BASE_URL}/audios/recorded", files=files, data=data
            )
            response.raise_for_status()

        else:
            response = requests.post(
                f"{API_BASE_URL}/audios/uploaded", data={"ori_audio_path": audio_path}
            )
            response.raise_for_status()

    except Exception as e:
        st.error(f"오디오 preprocessing 중 문제가 발생했습니다: {e}")
        raise ValueError(
            f"STT 진행 중에 문제가 발생했습니다: project interview_slug_id-{interview_slug_id}\n{e}"
        )

    return response.json()


def transcript(audio_path: str) -> STTResponse:

    try:
        response = requests.post(
            f"{API_BASE_URL}/transcripts/stt", json={"resampled_audio_path": audio_path}
        )
        response.raise_for_status()

    except Exception as e:
        st.error(f"오디오 STT 중 문제가 발생했습니다: {e}")
        raise ValueError(f"STT 진행 중에 문제가 발생했습니다: {audio_path}\n{e}")

    return response.json()


def stt(interview_slug_id: str, audio_byte: Optional[bytes]) -> STTResponse:

    msg = preprocess_audio(
        interview_slug_id,
        audio_byte=audio_byte,
    )

    msg = transcript(msg["resampled_audio_path"])

    return msg
