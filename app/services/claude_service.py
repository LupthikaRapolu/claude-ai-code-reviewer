import anthropic
from typing import AsyncGenerator
from app.config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _build_code_block(code: str, language: str) -> str:
    lang = "" if language == "unknown" else language
    return f"```{lang}\n{code}\n```"


def call_claude(system_prompt: str, user_message: str) -> dict:
    """Non-streaming call. Returns result text and token usage."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text

    return {
        "result": result,
        "model": MODEL,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


def stream_claude(system_prompt: str, user_message: str) -> AsyncGenerator[str, None]:
    """Returns a context-manager stream for SSE responses."""
    return client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )


# ── Review ────────────────────────────────────────────────────────────────────

REVIEW_SYSTEM = """You are an expert code reviewer with deep knowledge across all major
programming languages and paradigms. Your reviews are thorough, constructive, and actionable.

Structure every review with these sections:
## Summary
Brief overall assessment (2-3 sentences).

## Issues Found
List each issue with:
- **Severity**: Critical / Major / Minor / Suggestion
- **Location**: Line or function name if identifiable
- **Description**: Clear explanation of the problem
- **Fix**: Concrete recommendation

## Security Concerns
Highlight any security vulnerabilities or risks.

## Performance Notes
Comment on algorithmic complexity and performance considerations.

## Code Quality
Observations on readability, maintainability, naming, and structure.

## Positive Highlights
What the code does well.

Be direct and specific. Prioritize actionable feedback."""


def build_review_message(code: str, language: str, context: str | None, focus: str | None) -> str:
    parts = []
    if context:
        parts.append(f"**Context:** {context}")
    if focus:
        parts.append(f"**Review focus:** {focus}")
    parts.append(f"Please review this {language} code:\n\n{_build_code_block(code, language)}")
    return "\n\n".join(parts)


# ── Explain ───────────────────────────────────────────────────────────────────

EXPLAIN_SYSTEM = """You are a patient and precise software educator who specialises in making
code understandable to developers at all experience levels.

Structure every explanation with these sections:
## Overview
What this code does in plain English (2-4 sentences).

## How It Works — Step by Step
Walk through the logic in execution order. Explain key decisions and patterns used.

## Key Concepts
Call out important language features, design patterns, or algorithms at play.

## Inputs & Outputs
What the code expects and what it produces.

## Edge Cases & Assumptions
What assumptions the code makes; how it handles (or doesn't handle) edge cases.

## Example Usage
A short illustrative usage example if helpful.

Favour clarity. Define jargon the first time you use it."""


def build_explain_message(code: str, language: str, context: str | None) -> str:
    parts = []
    if context:
        parts.append(f"**Context:** {context}")
    parts.append(f"Please explain this {language} code:\n\n{_build_code_block(code, language)}")
    return "\n\n".join(parts)


# ── Unit Tests ────────────────────────────────────────────────────────────────

TESTS_SYSTEM = """You are a senior software engineer who specialises in test-driven development
and writing comprehensive, maintainable test suites.

When generating unit tests:
- Cover happy paths, edge cases, and error/exception paths
- Use descriptive test names that read like sentences
- Add a brief comment above each test explaining what it verifies
- Group related tests in classes or describe blocks where appropriate
- Mock external dependencies; keep tests isolated and fast
- Aim for high but meaningful coverage — quality over quantity

Respond with ONLY the test file content (no extra prose), preceded by a short header comment
listing the framework used and any install instructions."""


def build_tests_message(code: str, language: str, context: str | None, framework: str | None) -> str:
    parts = []
    if context:
        parts.append(f"**Context:** {context}")
    if framework:
        parts.append(f"**Test framework:** {framework}")
    parts.append(
        f"Generate comprehensive unit tests for this {language} code:\n\n"
        f"{_build_code_block(code, language)}"
    )
    return "\n\n".join(parts)


# ── Improve ───────────────────────────────────────────────────────────────────

IMPROVE_SYSTEM = """You are a senior software engineer performing a code improvement pass.
Your job is to return measurably better code along with a clear explanation of every change.

Structure your response with:
## Improved Code
The full, improved version of the code in a fenced code block.

## Changes Made
A numbered list of every change, explaining:
- **What** was changed
- **Why** it is better (correctness, readability, performance, security, etc.)

## Before / After Highlights
For the most impactful changes, show a short before/after snippet.

Rules:
- Preserve the original behaviour unless a bug fix is clearly needed
- Do not over-engineer; improvements must be justified
- Keep the same language and framework unless a change is explicitly requested"""


def build_improve_message(code: str, language: str, context: str | None, goals: str | None) -> str:
    parts = []
    if context:
        parts.append(f"**Context:** {context}")
    if goals:
        parts.append(f"**Improvement goals:** {goals}")
    parts.append(
        f"Please improve this {language} code:\n\n{_build_code_block(code, language)}"
    )
    return "\n\n".join(parts)
