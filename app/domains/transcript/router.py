import os
import subprocess
import json

from fastapi import APIRouter, HTTPException, Query, Depends

from app.domains.transcript.service import TranscriptService
from app.domains.transcript.schema import (
    STTRequest,
    STTResponse,
    MessageResponse,
    MessageRequest,
)

from app.core.config import settings
from app.database import get_db

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


def get_transcript_service(
    # config=Depends(get_config),
) -> TranscriptService:

    return TranscriptService()


@router.post("", response_model=MessageResponse)
def create_message(
    data: MessageRequest,
    service: TranscriptService = Depends(get_transcript_service),
    db=Depends(get_db),
) -> MessageResponse:

    response = service.create_message(data, db)

    return response


@router.patch("/{message_id}", response_model=MessageResponse)
def update_message(
    message_id: int,
    data: MessageRequest,
    service: TranscriptService = Depends(get_transcript_service),
    db=Depends(get_db),
):
    return service.update_message(message_id, data.content, db)


@router.delete("/{message_id}", status_code=204)
def delete_message(
    message_id: int,
    service: TranscriptService = Depends(get_transcript_service),
    db=Depends(get_db),
):

    service.delete_message(message_id, db)

    return None


@router.post("/stt", response_model=STTResponse)
def stt(
    data: STTRequest, service: TranscriptService = Depends(get_transcript_service)
) -> STTResponse:

    response = service.stt(data)

    return response
