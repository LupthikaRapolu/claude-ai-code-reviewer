from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import ImproveRequest, CodeResponse
from app.services.claude_service import (
    call_claude,
    stream_claude,
    IMPROVE_SYSTEM,
    build_improve_message,
)

router = APIRouter(prefix="/improve", tags=["Improve"])


@router.post("", response_model=CodeResponse, summary="Improve code quality, readability and performance")
def improve_code(request: ImproveRequest) -> CodeResponse:
    message = build_improve_message(
        request.code, request.language, request.context, request.goals
    )
    data = call_claude(IMPROVE_SYSTEM, message)
    return CodeResponse(**data)


@router.post("/stream", summary="Stream code improvements (Server-Sent Events)")
def improve_code_stream(request: ImproveRequest) -> StreamingResponse:
    message = build_improve_message(
        request.code, request.language, request.context, request.goals
    )

    def generate():
        with stream_claude(IMPROVE_SYSTEM, message) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/event-stream")
