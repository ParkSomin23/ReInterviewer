import streamlit as st

import requests
import math
import random
import time

from typing import Optional, Union, List
from collections import defaultdict

import json
import logging

from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# FastAPI 서버 URL (환경 변수로 설정 가능)
API_BASE_URL = "http://localhost:8000"


def main():
    # 페이지 정의
    dash_page = st.Page(
        "streamlit_views/dashboard.py", title="내 면접 목록", icon="📊", default=True
    )
    intv_page = st.Page(
        "streamlit_views/user_projects.py", title="새 면접 복기", icon="🎙️"
    )

    # 네비게이션 구성 (사이드바를 숨기고 싶다면 position="hidden" 추가 가능)
    pg = st.navigation([dash_page, intv_page], position="hidden")
    pg.run()


# def init_session_state():
#     """
#     화면 상태 초기화
#     """

#     # 랜덤 모드 상태 초기화
#     if "random_mode" not in st.session_state:
#         st.session_state.random_mode = False

#     # 선택된 책 저장
#     if "show_book_list" not in st.session_state:
#         st.session_state.show_book_list = None

#     if "selected_book_id" not in st.session_state:
#         st.session_state.selected_book_id = None

#     if "selected_book_title" not in st.session_state:
#         st.session_state.selected_book_title = None

#     if "recommended_book_list" not in st.session_state:
#         st.session_state.recommended_book_list = None

#     # dialog 상태 관리
#     if "dialog_mode" not in st.session_state:
#         st.session_state.dialog_mode = None

#     # 페이지 새로고침 시 dialog 자동 닫기
#     if "page_loaded" not in st.session_state:
#         st.session_state.page_loaded = True
#         # 페이지가 새로 로드되었을 때 dialog 닫기

#     if "search_doc" not in st.session_state:
#         st.session_state.search_doc = None

#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "채팅 기반 책 추천을 진행합니다. 재밌게 읽은 책에 대해서 알려주세요! 👇",
#             }
#         ]


# def main():

#     st.title("ReInterviewer")
#     st.subheader("나만의 면접 복기 친구")

#     chat_container = st.container(border=True, height=420)
#     input_container = st.container()
#     uploaded_file = st.file_uploader("오디오 파일을 올려주세요")

#     if uploaded_file:
#         # FastAPI 백엔드로 파일 전송
#         files = {"file": uploaded_file.getvalue()}
#         response = requests.post(API_BASE_URL, files=files)
#         st.write(response.json()["summary"])

#     with chat_container:
#         # Display chat messages from history on app rerun
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#     with input_container:
#         prompt = st.chat_input("I want to read a book about...")

#     if prompt:
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Display user message in chat message container
#         with chat_container:
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             # Display assistant response in chat message container
#             with st.chat_message("assistant"):
#                 message_placeholder = st.empty()
#                 full_response = ""
#                 assistant_response = random.choice(
#                     [
#                         "Press '책 추천 받기' button to get books recommended based on the conversation. If you want to add more information, continue the chat.",
#                     ]
#                 )
#                 # Simulate stream of response with milliseconds delay
#                 for chunk in assistant_response.split():
#                     full_response += chunk + " "
#                     time.sleep(0.05)
#                     # Add a blinking cursor to simulate typing
#                     message_placeholder.markdown(full_response + "▌")
#                 message_placeholder.markdown(full_response)

#                 st.button(
#                     "책 추천 받기",
#                     use_container_width=True,
#                     key="recommend_button",
#                     on_click=None,
#                     args=("from_chat_recommend", None, st.session_state.messages),
#                 )

#                 # Add assistant response to chat history
#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": full_response}
#                 )


if __name__ == "__main__":

    # API 연결 확인
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            st.error(
                "⚠️ FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."
            )
            st.stop()

    except Exception as e:
        st.error(f"⚠️ FastAPI 서버에 연결할 수 없습니다: {e}")
        st.info("💡 FastAPI 서버를 실행하려면: `uvicorn app.main:app --reload`")
        st.stop()

    main()
