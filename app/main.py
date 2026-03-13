from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import anthropic

from app.routers import review, explain, tests, improve

app = FastAPI(
    title="AI Code Reviewer",
    description=(
        "A FastAPI application powered by Claude that reviews, explains, "
        "improves, and generates tests for your code."
    ),
    version="1.0.0",
)

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(review.router, prefix="/api")
app.include_router(explain.router, prefix="/api")
app.include_router(tests.router, prefix="/api")
app.include_router(improve.router, prefix="/api")


# ── Global error handlers ─────────────────────────────────────────────────────

@app.exception_handler(anthropic.AuthenticationError)
async def auth_error_handler(request: Request, exc: anthropic.AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": "Invalid Anthropic API key."})


@app.exception_handler(anthropic.RateLimitError)
async def rate_limit_handler(request: Request, exc: anthropic.RateLimitError):
    return JSONResponse(status_code=429, content={"detail": "Rate limit reached. Please retry later."})


@app.exception_handler(anthropic.BadRequestError)
async def bad_request_handler(request: Request, exc: anthropic.BadRequestError):
    return JSONResponse(status_code=400, content={"detail": str(exc.message)})


@app.exception_handler(anthropic.APIStatusError)
async def api_error_handler(request: Request, exc: anthropic.APIStatusError):
    return JSONResponse(
        status_code=502,
        content={"detail": f"Upstream API error ({exc.status_code}): {exc.message}"},
    )


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok"}
