"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI
from openai import OpenAIError

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the purpose of life?"},
]

try:
    if not client.api_key:
        raise ValueError("OpenAI API key not found in environment variables")

    response = client.chat.completions.create(model=MODEL, messages=messages)
    print(response.choices[0].message.content)

except OpenAIError as e:
    print(f"OpenAI API error occurred: {str(e)}")
except ValueError as e:
    print(f"Configuration error: {str(e)}")
