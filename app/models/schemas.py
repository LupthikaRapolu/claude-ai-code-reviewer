from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Language(str, Enum):
    python = "python"
    javascript = "javascript"
    typescript = "typescript"
    java = "java"
    go = "go"
    rust = "rust"
    cpp = "cpp"
    c = "c"
    csharp = "csharp"
    ruby = "ruby"
    php = "php"
    swift = "swift"
    kotlin = "kotlin"
    unknown = "unknown"


class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1, description="The source code to process")
    language: Language = Field(Language.unknown, description="Programming language of the code")
    context: Optional[str] = Field(None, description="Optional context or description about the code")


class ReviewRequest(CodeRequest):
    focus: Optional[str] = Field(
        None,
        description="Optional focus area: 'security', 'performance', 'style', 'logic', etc."
    )


class ImproveRequest(CodeRequest):
    goals: Optional[str] = Field(
        None,
        description="Optional improvement goals: 'readability', 'performance', 'security', etc."
    )


class TestRequest(CodeRequest):
    framework: Optional[str] = Field(
        None,
        description="Optional test framework to use (e.g., 'pytest', 'jest', 'junit')"
    )


class CodeResponse(BaseModel):
    result: str
    model: str
    input_tokens: int
    output_tokens: int
