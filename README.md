```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Works with openai, 400 error with AI gateway

Output from running:
```
(gateway-agents-bug-repro) ricardo@Ricardos-MacBook-Pro gateway-agents-bug-repro % uv run main.py
using openai
The capital of France is Paris. The current weather in Paris is sunny. 

If you need more details like temperature or forecast, let me know!


********** using Vercel AI Gateway **********



=== OpenAI HTTP Request ===
POST https://ai-gateway.vercel.sh/v1/chat/completions
Headers: {'host': 'ai-gateway.vercel.sh', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'accept': 'application/json', 'content-type': 'application/json', 'user-agent': 'Agents/Python 0.3.2', 'x-stainless-lang': 'python', 'x-stainless-package-version': '1.109.1', 'x-stainless-os': 'MacOS', 'x-stainless-arch': 'arm64', 'x-stainless-runtime': 'CPython', 'x-stainless-runtime-version': '3.11.13', 'x-stainless-async': 'async:asyncio', 'x-stainless-retry-count': '0', 'x-stainless-read-timeout': '60.0', 'content-length': '730'}
JSON Body:
{
  "messages": [
    {
      "content": "You provide help with math problems. Explain your reasoning at each step and include examples",
      "role": "system"
    },
    {
      "role": "user",
      "content": "What is the weather in the capital of France?"
    }
  ],
  "model": "gpt-4.1",
  "stream": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_capital",
        "description": "",
        "parameters": {
          "properties": {
            "country": {
              "title": "Country",
              "type": "string"
            }
          },
          "required": [
            "country"
          ],
          "title": "get_capital_args",
          "type": "object",
          "additionalProperties": false
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "",
        "parameters": {
          "properties": {
            "city": {
              "title": "City",
              "type": "string"
            }
          },
          "required": [
            "city"
          ],
          "title": "get_weather_args",
          "type": "object",
          "additionalProperties": false
        }
      }
    }
  ]
}
==========================


=== OpenAI HTTP Request ===
POST https://ai-gateway.vercel.sh/v1/chat/completions
Headers: {'host': 'ai-gateway.vercel.sh', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'accept': 'application/json', 'content-type': 'application/json', 'user-agent': 'Agents/Python 0.3.2', 'x-stainless-lang': 'python', 'x-stainless-package-version': '1.109.1', 'x-stainless-os': 'MacOS', 'x-stainless-arch': 'arm64', 'x-stainless-runtime': 'CPython', 'x-stainless-runtime-version': '3.11.13', 'x-stainless-async': 'async:asyncio', 'x-stainless-retry-count': '0', 'x-stainless-read-timeout': '60.0', 'content-length': '1004'}
JSON Body:
{
  "messages": [
    {
      "content": "You provide help with math problems. Explain your reasoning at each step and include examples",
      "role": "system"
    },
    {
      "role": "user",
      "content": "What is the weather in the capital of France?"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_z0KUeLafvAXcHZGoSRCwLZ81",
          "type": "function",
          "function": {
            "name": "get_capital",
            "arguments": "{\"country\":\"France\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_z0KUeLafvAXcHZGoSRCwLZ81",
      "content": "The capital of France is France."
    }
  ],
  "model": "gpt-4.1",
  "stream": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_capital",
        "description": "",
        "parameters": {
          "properties": {
            "country": {
              "title": "Country",
              "type": "string"
            }
          },
          "required": [
            "country"
          ],
          "title": "get_capital_args",
          "type": "object",
          "additionalProperties": false
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "",
        "parameters": {
          "properties": {
            "city": {
              "title": "City",
              "type": "string"
            }
          },
          "required": [
            "city"
          ],
          "title": "get_weather_args",
          "type": "object",
          "additionalProperties": false
        }
      }
    }
  ]
}
==========================

ERROR: Agents run via Vercel AI Gateway raised: BadRequestError("Error code: 400 - {'error': {'message': 'Invalid input', 'type': 'invalid_request_error', 'param': 'messages.2.content', 'code': 'invalid_request_error'}}")


********** sync Chat Completions repro (gateway) **********



=== OpenAI HTTP Request (sync) ===
POST https://ai-gateway.vercel.sh/v1/chat/completions
Headers: {'host': 'ai-gateway.vercel.sh', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'accept': 'application/json', 'content-type': 'application/json', 'user-agent': 'OpenAI/Python 1.109.1', 'x-stainless-lang': 'python', 'x-stainless-package-version': '1.109.1', 'x-stainless-os': 'MacOS', 'x-stainless-arch': 'arm64', 'x-stainless-runtime': 'CPython', 'x-stainless-runtime-version': '3.11.13', 'x-stainless-async': 'false', 'x-stainless-retry-count': '0', 'x-stainless-read-timeout': '60.0', 'content-length': '876'}
JSON Body:
{
  "messages": [
    {
      "role": "system",
      "content": "You provide help with math problems. Explain your reasoning at each step and include examples"
    },
    {
      "role": "user",
      "content": "What is the weather in the capital of France?"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_test",
          "type": "function",
          "function": {
            "name": "get_capital",
            "arguments": "{\"country\":\"France\"}"
          }
        }
      ]
    }
  ],
  "model": "gpt-4.1",
  "stream": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_capital",
        "description": "",
        "parameters": {
          "type": "object",
          "title": "get_capital_args",
          "properties": {
            "country": {
              "title": "Country",
              "type": "string"
            }
          },
          "required": [
            "country"
          ],
          "additionalProperties": false
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "",
        "parameters": {
          "type": "object",
          "title": "get_weather_args",
          "properties": {
            "city": {
              "title": "City",
              "type": "string"
            }
          },
          "required": [
            "city"
          ],
          "additionalProperties": false
        }
      }
    }
  ]
}
=================================

ERROR: Sync repro raised: BadRequestError("Error code: 400 - {'error': {'message': 'Invalid input', 'type': 'invalid_request_error', 'param': 'messages.2.content', 'code': 'invalid_request_error'}}")
(gateway-agents-bug-repro) ricardo@Ricardos-MacBook-Pro gateway-agents-bug-repro % 
```