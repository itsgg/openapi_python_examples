"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the purpose of life?"},
]

output = client.chat.completions.create(model=MODEL, messages=messages)

print(output)
