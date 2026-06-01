import re
import json

from pydantic import BaseModel

from ollama import chat, generate

from app.core.config import settings

import app.domains.llm.utils as utils
from app.domains.llm.prompts import interviewer, summarizer
from app.domains.llm.schema import (
    QuestionRequest,
    QuestionResponse,
    InterviewResponse,
    InterviewResponseList,
)

from app.domains.transcript.schema import MessageRequest, MessageResponse


class LLMService:
    def __init__(self):

        self.model = settings.LLM_MODEL
        self.options = settings.LLM_OPTIONS
        self.think = settings.LLM_THINKING
        self.stream = settings.LLM_STEAMING

    def generate_chat(self, request: list[MessageResponse]) -> str:

        msg = [interviewer.prompt] + request
        response = chat(
            model=self.model,
            options=self.options,
            think=self.think,
            stream=self.stream,
            messages=msg,
        )

        return response.message.content

    # 면접 질문 떠올릴 수 있는 질문 생성
    def generate_chat_response(self, request: QuestionRequest) -> QuestionResponse:
        """
        사용자의 이전 대화 기록을 바탕으로 면접 질문을 떠올릴 수 있는 말을 해줍니다.
        """

        msg = [interviewer.prompt] + request.chat_history
        response = chat(
            model=self.model,
            options=self.options,
            think=self.think,
            stream=self.stream,
            messages=msg,
        )

        return QuestionResponse(
            interview_slug=request.interview_slug,
            question_num=request.question_num,
            role="assistant",
            content=response.message.content,
        )

    # 면접 질문 하나에 대한 요약 정리
    def organize_interview_question(
        self, request: list[MessageResponse], use_chat=False
    ) -> InterviewResponse:
        """
        전체 대화 내용을 분석하여 잘한 점, 아쉬운 점, 키워드 등을 정형화된 데이터로 요약합니다.

        use_chat: If False, it uses generate function from ollama
        """

        schema_str, schema_dict = utils.clean_schema_format(InterviewResponse)

        system_msg = utils.get_system_prompt(
            prompt_template=summarizer.prompt_template, clean_schema_format=schema_str
        )

        # TODO: prompt / chat / generate 조건 분기

        if use_chat:
            msg_json = [system_msg] + [
                {"role": r.role, "content": r.content.strip()} for r in request
            ]

            response = chat(
                model=self.model,
                options=self.options,
                think=self.think,
                stream=self.stream,
                messages=msg_json,
                format=InterviewResponse.model_json_schema(),
            )
        else:

            usr_msg = [r.content.strip() for r in request if r.role == "user"]
            full_prompt = f"{system_msg}\n\nUser Conversations:\n" + "\n\n".join(
                usr_msg
            )

            response = generate(
                model=self.model,
                options=self.options,
                think=self.think,
                stream=self.stream,
                prompt=full_prompt,
                format=InterviewResponse.model_json_schema(),
            )

        final_json_string = utils.parse_interview_response(response, schema_dict)

        return InterviewResponse.model_validate_json(final_json_string)
