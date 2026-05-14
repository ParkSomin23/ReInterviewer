import os
import json
import requests

import streamlit as st

from app.domains.project.schema import InterviewResponse

API_BASE_URL = "http://localhost:8000"


def fetch_interview_list() -> list[InterviewResponse]:
    try:
        response = requests.get(f"{API_BASE_URL}/projects")
        response.raise_for_status()

        print(response.json())

        return response.json()

    except Exception as e:
        st.error(f"프로젝트 불러오는 중 문제가 발생했습니다: {e}")
        return None


def style():

    st.markdown(
        """
        <style>
        /* 1. 버튼을 감싸는 div의 간격 제거 */
        div.stButton {
            text-align: center;
            line-height: 1;
        }
        
        /* 2. 버튼 자체의 크기 및 패딩 강제 조정 */
        div.stButton > button {
            min-height: 0px !important;
            height: 1.6rem !important; /* 글자 크기보다 살짝 큰 정도로 유지 */
            padding: 0px 12px !important; /* 좌우 여백만 주고 상하는 0 */
            font-size: 10px !important; 
            line-height: 1.6rem !important;
            width: auto !important;
        }
        
        /* 3. 버튼이 행의 높이를 벌리지 않도록 마진 제거 */
        div.stButton > button:first-child {
            margin-top: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():

    st.set_page_config(layout="centered")

    st.title("📊 면접 복기 대시보드")
    st.write("이전에 진행했던 면접 기록들입니다.")

    # ➕ 새 면접 시작 버튼
    if st.button("➕ 새 면접 복기 시작하기", use_container_width=True):
        st.session_state.interview_id = None
        st.switch_page("streamlit_views/create_interview.py")

    st.divider()

    # 📋 기존 면접 리스트 출력
    interview_list = fetch_interview_list()

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
                st.switch_page("streamlit_views/projects/interview.py")


if __name__ == "__main__":
    style()
    main()
