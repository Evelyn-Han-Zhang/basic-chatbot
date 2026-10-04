import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("错误：没有读取到 OPENAI_API_KEY")
    sys.exit(1)

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
            "What is the current weather in Sydney, Australia? "
            "Give the temperature and weather conditions, and cite the source."
        ),
    },
    timeout=60,
)

if not response.ok:
    print(f"请求失败，状态码：{response.status_code}")
    print(response.text)
    sys.exit(1)

data = response.json()
used_web_search = any(
    item.get("type") == "web_search_call"
    for item in data.get("output", [])
)

print(f"Web search used: {used_web_search}")

for item in data.get("output", []):
    if item.get("type") != "message":
        continue

    for content in item.get("content", []):
        if content.get("type") == "output_text":
            print(content.get("text"))