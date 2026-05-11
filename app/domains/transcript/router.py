import os
import subprocess
import json

from fastapi import APIRouter, HTTPException, Query, Depends

from app.domains.transcript.service import STTService
from app.domains.transcript.schema import STTRequest, STTResponse

from app.core.config import settings

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


def get_stt_service(
    # config=Depends(get_config),
) -> STTService:
    """BookService 의존성 주입"""

    return STTService()


@router.post("/stt", response_model=STTResponse)
def stt(data: STTRequest, service: STTService = Depends(get_stt_service)) -> STTResponse:

    response = service.stt(data)

    return response
