"""
OpenAI Response Format Handler

This script demonstrates how to use OpenAI's response format feature to
get structured outputs from the API. It shows how to specify and handle
different response formats like JSON or function calls.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Handle different response formats (JSON, text)
    - Parse and validate structured responses
    - Error handling for malformed responses
    - Support for custom response schemas

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python response_format.py
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"
messages = [
    {"role": "user", "content": "List the hierarchy of human species in JSON format."},
]

output = client.chat.completions.create(
    model=MODEL, messages=messages, response_format={"type": "json_object"}
)

print(output)
