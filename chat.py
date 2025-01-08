"""
A simple OpenAI chat completion example using the OpenAI API.

This script demonstrates how to:
1. Initialize the OpenAI client
2. Set up a basic chat conversation
3. Handle API responses and errors

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Example:
    Set your OPENAI_API_KEY environment variable and run the script:
    $ export OPENAI_API_KEY='your-api-key'
    $ python chat.py
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
