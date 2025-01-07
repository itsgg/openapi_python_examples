"""
This is a simple example of how to use the OpenAI API wrapper.
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
