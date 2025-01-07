"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

transcript = client.audio.transcriptions.create(
    model="whisper-1", file=open("output.mp3", "rb")
)

print(transcript)
