from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import ReviewRequest, CodeResponse
from app.services.claude_service import (
    call_claude,
    stream_claude,
    REVIEW_SYSTEM,
    build_review_message,
)

router = APIRouter(prefix="/review", tags=["Review"])


@router.post("", response_model=CodeResponse, summary="Review code for bugs, issues and best practices")
def review_code(request: ReviewRequest) -> CodeResponse:
    message = build_review_message(
        request.code, request.language, request.context, request.focus
    )
    data = call_claude(REVIEW_SYSTEM, message)
    return CodeResponse(**data)


@router.post("/stream", summary="Stream a code review (Server-Sent Events)")
def review_code_stream(request: ReviewRequest) -> StreamingResponse:
    message = build_review_message(
        request.code, request.language, request.context, request.focus
    )

    def generate():
        with stream_claude(REVIEW_SYSTEM, message) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/event-stream")
