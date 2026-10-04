import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


load_dotenv()

app = FastAPI(
    title="Sydney Weather Chatbot",
    description="A basic chatbot using OpenAI Responses API and Web Search.",
)


class ChatRequest(BaseModel):
    message: str = "What is the current weather?"


def extract_output_text(data: dict) -> str:
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue

        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return " ".join(content.get("text", "").split())

    return ""


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured.",
        )

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4.1-mini",
            "instructions": (
                "You are a helpful general-purpose assistant. "
                "Reply in the same language as the user. "
                "Use web search only when the question requires current information."
            ),
            "tools": [
                {
                    "type": "web_search",
                }
            ],
            "tool_choice": "auto",
            "input": request.message,
        },
        timeout=60,
    )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail=response.text,
        )

    data = response.json()

    used_web_search = any(
        item.get("type") == "web_search_call"
        for item in data.get("output", [])
    )

    answer = extract_output_text(data)

    if not answer:
        raise HTTPException(
            status_code=502,
            detail="OpenAI returned no readable answer.",
        )

    return {
        "web_search_used": used_web_search,
        "answer": answer,
    }

@app.post("/chat/weather")
def chat_weather(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured.",
        )

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4.1-mini",
            "tools": [
                {
                    "type": "web_search",
                    "user_location": {
                        "type": "approximate",
                        "country": "AU",
                        "city": "Sydney",
                        "region": "New South Wales",
                        "timezone": "Australia/Sydney",
                    },
                }
            ],
            "tool_choice": "required",
            "input": (
                "Search the web for Sydney's weather right now. "
                "Answer in Chinese using exactly one short sentence. "
                "The sentence must contain the actual current weather condition, "
                "actual current temperature in Celsius, and today's actual low and high "
                "temperatures in Celsius. "
                "Never return blank fields, placeholders, headings, a map link, "
                "or a multi-day forecast. "
                "If a value cannot be found, write 暂无数据 instead of leaving it blank. "
                "End with one weather source link."
            ),
        },
        timeout=60,
    )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail=response.text,
        )

    data = response.json()

    used_web_search = any(
        item.get("type") == "web_search_call"
        for item in data.get("output", [])
    )

    answer = extract_output_text(data)

    if not answer:
        raise HTTPException(
            status_code=502,
            detail="OpenAI returned no readable answer.",
        )

    return {
        "city": "Sydney",
        "web_search_used": used_web_search,
        "answer": answer,
    }