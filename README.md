# Basic Chatbot Demo

A small FastAPI chatbot built with the OpenAI Responses API and hosted web search.

## Features

- `POST /chat` accepts general questions and lets the model decide when web search is needed.
- `POST /chat/weather` forces a live web search for current Sydney weather.
- `GET /health` provides a basic health check.
- Swagger UI provides an interactive interface for testing the API.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file or expose your API key.

Start the server:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open the Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Example request

Send the following request through `POST /chat`:

```json
{
  "message": "Explain machine learning in simple terms."
}
```

The response includes the generated answer and whether web search was used.
