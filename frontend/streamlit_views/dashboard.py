import os
import json
import requests

import streamlit as st

from app.domains.project.schema import InterviewResponse

API_BASE_URL = "http://localhost:8000"

st.title("📊 면접 복기 대시보드")
st.write("이전에 진행했던 면접 기록들입니다.")


def fetch_interview_list() -> list[InterviewResponse]:
    try:
        response = requests.get(f"{API_BASE_URL}/projects")
        response.raise_for_status()

        print(response.json())

        return response.json()

    except Exception as e:
        st.error(f"프로젝트 불러오는 중 문제가 발생했습니다: {e}")
        return None


# ➕ 새 면접 시작 버튼
if st.button("➕ 새 면접 복기 시작하기", use_container_width=True):
    # st.query_params.interview_id = None  # 새 면접임을 표시
    st.session_state.interview_id = None
    st.switch_page("streamlit_views/user_projects.py")

st.divider()

# 📋 기존 면접 리스트 출력
interview_list = fetch_interview_list()
st.write(len(interview_list))

col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

with col1:
    st.write(f"**회사 명**")

with col2:
    st.write(f"**면접일**")

with col3:
    st.write(f"**생성일**")

with col4:
    st.write(f"**프로젝트**")

for item in interview_list:

    with col1:
        st.write(item["company_name"])

    with col2:
        interview_date, interview_time = item["interview_date"].split("T")
        interview_time = interview_time[:-3]
        st.write(f"""{interview_date}\t{interview_time}""")

    with col3:
        created_date, created_time = item["created_at"].split("T")
        created_time = created_time.split(".")[0]
        st.write(f"""{created_date}\t{created_time}""")

    with col4:
        if st.button("보기", key=f"btn_{item['slug']}"):
            # st.query_params.interview_id = item["id"]
            st.session_state.interview_slug = item["slug"]
            st.switch_page("streamlit_views/user_projects.py")
