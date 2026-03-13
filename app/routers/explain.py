from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import CodeRequest, CodeResponse
from app.services.claude_service import (
    call_claude,
    stream_claude,
    EXPLAIN_SYSTEM,
    build_explain_message,
)

router = APIRouter(prefix="/explain", tags=["Explain"])


@router.post("", response_model=CodeResponse, summary="Explain what code does in plain English")
def explain_code(request: CodeRequest) -> CodeResponse:
    message = build_explain_message(request.code, request.language, request.context)
    data = call_claude(EXPLAIN_SYSTEM, message)
    return CodeResponse(**data)


@router.post("/stream", summary="Stream a code explanation (Server-Sent Events)")
def explain_code_stream(request: CodeRequest) -> StreamingResponse:
    message = build_explain_message(request.code, request.language, request.context)

    def generate():
        with stream_claude(EXPLAIN_SYSTEM, message) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/event-stream")
