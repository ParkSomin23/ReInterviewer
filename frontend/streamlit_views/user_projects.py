import streamlit as st
from streamlit_mic_recorder import mic_recorder

import io
import os
import random
import requests
import time

from pathlib import Path
from typing import Optional

from datetime import datetime
from nanoid import generate

from app.core.config import settings
from app.domains.project.schema import InterviewResponse
from app.domains.transcript.schema import STTRequest, STTResponse

API_BASE_URL = "http://localhost:8000"
PROJ_PATH = settings.proj_path


def init_session():

    st.set_page_config(layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    if "last_processed_audio" not in st.session_state:
        st.session_state.last_processed_audio = None

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None


@st.cache_data
def get_interview(slug: str) -> InterviewResponse:

    try:
        response = requests.get(f"{API_BASE_URL}/projects/{slug}")
        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"프로젝트 불러오는 중 문제가 발생했습니다: {e}")
        raise ValueError(
            f"인터뷰 프로젝트를 불러오는데 문제가 발생했습니다: project slug-{slug}\n{e}"
        )


# def save_uploaded_file(directory, file):

#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     with open(os.path.join(directory, file.name), "wb") as f:
#         f.write(file.getbuffer())

#     return st.success(f"파일 저장 완료: {directory}/{file.name}")


def load_interview(slug: str):
    proj_path = Path(settings.proj_path) / slug


def preprocess_audio(slug: str, audio_byte: Optional[bytes] = None) -> STTRequest:

    try:
        audio_name = generate(size=15) + ".wav"
        audio_path = Path(settings.proj_path) / slug / "audios" / audio_name

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
        raise ValueError(f"STT 진행 중에 문제가 발생했습니다: project slug-{slug}\n{e}")

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


def stt(slug: str, audio_byte: Optional[bytes]) -> STTResponse:

    msg = preprocess_audio(
        slug,
        audio_byte=audio_byte,
    )

    msg = transcript(msg["resampled_audio_path"])

    return msg


def main():

    st.header("🎙️ 면접 썰 풀기")
    st.write("친구에게 이야기하듯 편하게 말씀해주세요.")

    interview_slug = st.session_state.get("interview_slug")
    item = get_interview(interview_slug)

    st.subheader(f"{item['company_name']}: {item['position']} 인터뷰")

    # 화면
    header = st.container()
    col_input, col_rec = st.columns([0.85, 0.15])
    with col_rec:
        # 녹음 버튼
        audio_record = mic_recorder(
            start_prompt="🔴 Record",
            stop_prompt="⏹️ Stop",
            key="recorder",
            format="wav",
            use_container_width=True,
        )

    with col_input:
        chat_input = st.chat_input("답변을 입력하거나 마이크를 눌러 녹음하세요...")

    uploaded_file = st.file_uploader(
        "목소리 파일 업로드", type=["mp3", "wav", "m4a"], label_visibility="collapsed"
    )
    # if uploaded_file:
    #     audio_folder = PROJ_PATH / interview_slug / "audios"
    # save_uploaded_file(audio_folder, uploaded_file)

    # 입력 로직
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        st.rerun()

    elif audio_record:
        current_audio_id = audio_record.get("id")

        if current_audio_id != st.session_state.last_processed_audio:
            with st.spinner("음성을 텍스트로 변환 중입니다..."):
                audio_bytes = audio_record["bytes"]
                msg = stt(interview_slug, audio_byte=audio_bytes)

                msg_text = "🎙️ 음성 답변이 기록되었습니다.\n\n" + " ".join(msg["texts"])

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": msg_text,
                        "audio": audio_bytes,
                    }
                )

                st.session_state.last_processed_audio = current_audio_id
                st.rerun()

    elif uploaded_file:
        if st.session_state.last_uploaded_file != uploaded_file.name:
            with st.spinner("파일을 분석하여 텍스트로 변환 중입니다..."):
                audio_bytes = uploaded_file.read()

                # STT 수행
                msg = stt(interview_slug, audio_byte=audio_bytes)
                msg_text = "📁 업로드된 음성 답변이 기록되었습니다.\n\n" + " ".join(
                    msg["texts"]
                )

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": msg_text,
                        "audio": audio_bytes,
                    }
                )

                # 처리 완료 기록 및 상태 초기화
                st.session_state.last_uploaded_file = uploaded_file.name

                # 파일 업로더 UI를 초기화하고 메시지를 즉시 보여주기 위해 rerun
                st.rerun()

    # 뒤로가기 버튼 (대시보드로 복귀)
    if st.button("⬅️ 목록으로 돌아가기"):
        st.session_state.interview_id = None
        st.switch_page("streamlit_views/dashboard.py")

    with header:
        # 나중에 영상 서비스 연동 시 이 부분을 st.video나 커스텀 HTML로 교체
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            st.image("data/character.png", width=300)  # 현재는 이미지 한 개
            # st.markdown(
            #     "<h3 style='text-align: center;'>AI 면접관</h3>", unsafe_allow_html=True
            # )

        with col2:
            chat_container = st.container(border=True, height=300)
            with chat_container:
                for idx, message in enumerate(st.session_state.messages):
                    with st.chat_message(message["role"]):

                        # 1. 수정 중일 때: 전체 행을 하나의 폼으로 감쌉니다.
                        if st.session_state.editing_index == idx:
                            with st.form(key=f"edit_form_{idx}"):
                                # 폼 안에서 컬럼을 나눕니다.
                                msg_col, btn_col = st.columns([0.8, 0.2])

                                with msg_col:
                                    new_content = st.text_area(
                                        "메시지 수정",
                                        value=message["content"],
                                        label_visibility="collapsed",
                                    )

                                with btn_col:
                                    # 이제 버튼들이 폼 내부에 있으므로 정상 작동합니다.
                                    if st.form_submit_button("Save", icon="✅"):
                                        st.session_state.messages[idx][
                                            "content"
                                        ] = new_content
                                        st.session_state.editing_index = None
                                        st.rerun()

                                    if st.form_submit_button("Cancel", icon="❌"):
                                        st.session_state.editing_index = None
                                        st.rerun()

                        # 2. 일반 메시지 표시일 때
                        else:
                            msg_col, btn_col = st.columns([0.85, 0.15])
                            with msg_col:
                                st.markdown(message["content"])

                            with btn_col:
                                if message["role"] == "user":
                                    if st.button(
                                        "Edit", icon="✏️", key=f"edit_btn_{idx}"
                                    ):
                                        st.session_state.editing_index = idx
                                        st.rerun()

        st.divider()


if __name__ == "__main__":
    init_session()
    main()
