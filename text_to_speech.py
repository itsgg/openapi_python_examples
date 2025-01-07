"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.audio.speech.create(
    model="tts-1", input="A man is walking down the street.", voice="alloy"
)

with open("output.mp3", "wb") as file:
    file.write(response.content)
