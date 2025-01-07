"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.moderations.create(
    model="omni-moderation-latest", input="I want to kill my neighbour."
)

print(response.results[0])
