from pydantic import BaseModel, Field
from app.domains.transcript.schema import MessageResponse


# 면접 질문 당 정리
class InterviewResponse(BaseModel):

    question: str = Field(description="면접관이 던진 핵심 질문 문장")
    user_answer: str | None = Field(description="질문에 대한 사용자의 답변 내용")
    interviewer_reaction: str | None = Field(description="면접관의 반응 및 태도")
    self_evaluation: str | None = Field(description="답변에 대한 본인의 피드백/생각")
    etc: str | None


class InterviewResponseList(BaseModel):
    interview_data: list[InterviewResponse]


# question_generator
class QuestionRequest(BaseModel):

    interview_slug: int
    question_num: int = Field(description="면접 질문 번호")

    current_question: str | None = Field(
        description="현재 면접 질문, 없다면 질문을 떠올릴 수 있게 유도"
    )
    chat_history: list[dict] | None = Field(
        description="현재 면접 질문에 대한 대화 내용"
    )

    previous_question_list: list[str] | None = Field(
        description="이전 면접 질문 리스트"
    )


class QuestionResponse(BaseModel):

    interview_slug: int
    question_num: int = Field(description="면접 질문 번호")

    role: str = Field(description="llm 응답 role")
    content: str = Field(description="llm 응답 내용")
