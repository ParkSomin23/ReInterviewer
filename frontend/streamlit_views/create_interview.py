import streamlit as st
import datetime

from app.domains.project.schema import InterviewCreate
from frontend.api import create_interview

char_img = "data/character.png"


def init_session():

    st.set_page_config(layout="centered")

    if "question_list" not in st.session_state:
        st.session_state.question_list = [
            "면접본 회사 이름은 무엇인가요?",
            "어떤 직종으로 면접을 보셨나요?",
            "언제 면접을 봤나요?",
            # "더 남기고 싶은 말이 있나요?", TODO: 더 기능 추가 시..
        ]


def main():

    # =========== 화면 구성 ===========
    st.header("🎙️ 면접 정보 입력")
    st.write("함께 이야기할 면접에 대해서 기본적인 정보를 알려주세요")

    header = st.container()
    with header:

        with st.form("create_new_interview"):
            st.write(st.session_state.question_list[0])
            company = st.text_input(
                "면접 본 회사 이름을 작성해주세요",
                label_visibility="collapsed",
            )

            st.write(st.session_state.question_list[1])
            position = st.text_input(
                "면접본 직종을 작성해주세요",
                label_visibility="collapsed",
            )

            st.write(st.session_state.question_list[2])
            event_time = st.datetime_input(
                "면접 본 날짜를 선택해주세요",
                step=15 * 60,
                label_visibility="collapsed",
            )

            b_col1, b_col2, b_col3 = st.columns([5, 2, 2])

            with b_col2:
                summit = st.form_submit_button("다음 단계", icon="➡️", width="stretch")

            with b_col3:
                cancel = st.form_submit_button("취소", icon="❌", width="stretch")

            if summit:
                if not company or not position:
                    st.warning("회사명과 직무를 모두 입력해주세요.")
                    st.stop()

                event_time_str = event_time.isoformat()

                st.success(
                    f"{company}: {position} 인터뷰를 생성합니다. ({event_time_str})"
                )

                response = create_interview(
                    InterviewCreate(
                        company_name=company.strip(),
                        position=position.strip(),
                        interview_date=event_time_str,
                    )
                )

                if response:
                    st.session_state.interview_slug = response["slug"]
                    st.switch_page("streamlit_views/projects/interview.py")

            if cancel:
                st.switch_page("streamlit_views/dashboard.py")


if __name__ == "__main__":
    init_session()
    main()
