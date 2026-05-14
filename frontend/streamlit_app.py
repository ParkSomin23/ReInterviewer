import streamlit as st

import requests
import logging

logger = logging.getLogger(__name__)

# FastAPI 서버 URL (환경 변수로 설정 가능)
API_BASE_URL = "http://localhost:8000"


def main():

    dash_page = st.Page(
        "streamlit_views/dashboard.py", title="내 면접 목록", icon="📊", default=True
    )
    intv_page = st.Page(
        "streamlit_views/projects/interview.py", title="새 면접 복기", icon="🎙️"
    )

    create_page = st.Page(
        "streamlit_views/create_interview.py", title="새 면접 복기", icon="🎙️"
    )

    pg = st.navigation([dash_page, create_page, intv_page], position="hidden")
    pg.run()


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
