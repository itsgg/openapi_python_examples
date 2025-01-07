"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

with open("output.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(transcript.text)
