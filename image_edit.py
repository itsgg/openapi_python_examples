"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.images.edit(
    image=open("output.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="A indian man is walking down the street.",
)

print(response.data[0].url)
