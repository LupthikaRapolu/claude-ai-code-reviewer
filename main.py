from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI
import anthropic
import time
import os
from dotenv import load_dotenv

from prompts import (
    review_code_prompt,
    explain_code_prompt,
    generate_tests_prompt,
    improve_code_prompt
)

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Review code endpoint
@app.post("/review")
async def review_code(code: str):

    prompt = review_code_prompt(code)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return {"review": response.content}


# Explain code endpoint
@app.post("/explain")
async def explain_code(code: str):

    prompt = explain_code_prompt(code)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return {"explanation": response.content}


# Generate tests endpoint
@app.post("/generate-tests")
async def generate_tests(code: str):

    prompt = generate_tests_prompt(code)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return {"tests": response.content}


# Improve code endpoint
@app.post("/improve")
async def improve_code(code: str):

    prompt = improve_code_prompt(code)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return {"improved_code": response.content}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})