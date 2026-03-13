from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import TestRequest, CodeResponse
from app.services.claude_service import (
    call_claude,
    stream_claude,
    TESTS_SYSTEM,
    build_tests_message,
)

router = APIRouter(prefix="/tests", tags=["Unit Tests"])


@router.post("", response_model=CodeResponse, summary="Generate unit tests for the provided code")
def generate_tests(request: TestRequest) -> CodeResponse:
    message = build_tests_message(
        request.code, request.language, request.context, request.framework
    )
    data = call_claude(TESTS_SYSTEM, message)
    return CodeResponse(**data)


@router.post("/stream", summary="Stream unit test generation (Server-Sent Events)")
def generate_tests_stream(request: TestRequest) -> StreamingResponse:
    message = build_tests_message(
        request.code, request.language, request.context, request.framework
    )

    def generate():
        with stream_claude(TESTS_SYSTEM, message) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/event-stream")
