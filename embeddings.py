"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

result = client.embeddings.create(
    input="The food was delicious and the waiter...", model="text-embedding-3-small"
)

print(result)
