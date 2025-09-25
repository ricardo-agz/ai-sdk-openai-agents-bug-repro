from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
import asyncio
import os
import json
import httpx


load_dotenv()


async def log_request(request: httpx.Request) -> None:
    safe_headers = {k: v for k, v in request.headers.items() if k.lower() != "authorization"}
    try:
        raw = request.content or b""
        body = json.loads(raw.decode("utf-8") or "{}")
        body_str = json.dumps(body, indent=2)
    except Exception:
        body_str = (request.content or b"").decode("utf-8", errors="replace")

    print("\n=== OpenAI HTTP Request ===")
    print(f"{request.method} {request.url}")
    print(f"Headers: {safe_headers}")
    print("JSON Body:")
    print(body_str)
    print("==========================\n")

def log_request_sync(request: httpx.Request) -> None:
    safe_headers = {k: v for k, v in request.headers.items() if k.lower() != "authorization"}
    try:
        raw = request.content or b""
        body = json.loads(raw.decode("utf-8") or "{}")
        body_str = json.dumps(body, indent=2)
    except Exception:
        body_str = (request.content or b"").decode("utf-8", errors="replace")

    print("\n=== OpenAI HTTP Request (sync) ===")
    print(f"{request.method} {request.url}")
    print(f"Headers: {safe_headers}")
    print("JSON Body:")
    print(body_str)
    print("=================================\n")

@function_tool
def get_capital(country: str) -> str:
    return f"The capital of {country} is {country.capitalize()}."


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    tools=[get_capital, get_weather],
)


async def main():
    if os.getenv("OPENAI_API_KEY"):
        # this works
        print("using openai")
        result = await Runner.run(agent, "What is the weather in the capital of France?")
        print(result.final_output)

    # this doesn't work
    print("\n\n********** using Vercel AI Gateway **********\n\n")
    api_key = os.getenv("AI_GATEWAY_API_KEY") or os.getenv("VERCEL_OIDC_TOKEN")
    base_url = "https://ai-gateway.vercel.sh/v1"
    if not api_key:
        raise ValueError("AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN is not set")

    async with httpx.AsyncClient(
        timeout=60.0,
        event_hooks={"request": [log_request]},
    ) as http_client:
        client = AsyncOpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
        set_default_openai_client(client=client, use_for_tracing=False)
        set_default_openai_api("chat_completions")
        set_tracing_disabled(disabled=True)

        try:
            result = await Runner.run(agent, "What is the weather in the capital of France?")
            print(result.final_output)
        except Exception as e:
            print("ERROR: Agents run via Vercel AI Gateway raised:", repr(e))

    # Sync Chat Completions repro using the problematic message shape
    print("\n\n********** sync Chat Completions repro (gateway) **********\n\n")
    messages = [
        {
            "role": "system",
            "content": "You provide help with math problems. Explain your reasoning at each step and include examples",
        },
        {
            "role": "user",
            "content": "What is the weather in the capital of France?",
        },
        {
            "role": "assistant",
            # Intentionally no 'content' to replicate the 400 error
            "tool_calls": [
                {
                    "id": "call_test",
                    "type": "function",
                    "function": {
                        "name": "get_capital",
                        "arguments": "{\"country\":\"France\"}",
                    },
                }
            ],
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_capital",
                "description": "",
                "parameters": {
                    "type": "object",
                    "title": "get_capital_args",
                    "properties": {"country": {"title": "Country", "type": "string"}},
                    "required": ["country"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "",
                "parameters": {
                    "type": "object",
                    "title": "get_weather_args",
                    "properties": {"city": {"title": "City", "type": "string"}},
                    "required": ["city"],
                    "additionalProperties": False,
                },
            },
        },
    ]

    with httpx.Client(timeout=60.0, event_hooks={"request": [log_request_sync]}) as sync_http:
        sync_client = OpenAI(api_key=api_key, base_url=base_url, http_client=sync_http)
        try:
            completion = sync_client.chat.completions.create(
                model="gpt-4.1",
                messages=messages,
                tools=tools,
                stream=False,
            )
            print(completion.choices[0].message)
        except Exception as e:
            print("ERROR: Sync repro raised:", repr(e))


if __name__ == "__main__":
    asyncio.run(main())
