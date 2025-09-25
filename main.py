from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio
import os


load_dotenv()


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
        print("using openai")
        result = await Runner.run(agent, "What is the weather in the capital of France?")
        print(result.final_output)

    print("using openai gateway")
    api_key = os.getenv("AI_GATEWAY_API_KEY") or os.getenv("VERCEL_OIDC_TOKEN")
    base_url = "https://ai-gateway.vercel.sh/v1"
    if not api_key:
        raise ValueError("AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN is not set")

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(disabled=True)

    result = await Runner.run(agent, "What is the weather in the capital of France?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
