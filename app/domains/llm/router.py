from fastapi import APIRouter, HTTPException, Query, Depends

from app.domains.llm.schema import InterviewResponse
from app.domains.llm.service import LLMService

from app.domains.transcript.schema import MessageResponse

router = APIRouter(prefix="/llm", tags=["llm"])


def get_llm_service() -> LLMService:
    """BookService 의존성 주입"""

    return LLMService()


@router.post("/summarize/full", response_model=InterviewResponse)
def summarize_interview(
    service: LLMService = Depends(get_llm_service),
):

    raise NotImplementedError


@router.post("/summarize/part", response_model=InterviewResponse)
def summarize_question(
    request: list[MessageResponse],
    use_chat: bool,
    service: LLMService = Depends(get_llm_service),
):

    return service.organize_interview_question(request=request, use_chat=use_chat)


@router.post("/chat")
def generate_chat_response(
    request: list[MessageResponse],
    service: LLMService = Depends(get_llm_service),
) -> str:

    return service.generate_chat(request)  # , use_chat=use_chat)


# @router.post("/ask", response_model=InterviewResponse)
# def generate_chat_response(
#     request: list[MessageResponse],
#     use_chat: bool,
#     service: LLMService = Depends(get_llm_service),
# ):

#     print("########router", request)

#     return service.generate_chat_response(request)  # , use_chat=use_chat)

# @router.get("", response_model=)
# def get_
