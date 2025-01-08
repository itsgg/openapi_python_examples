"""
OpenAI Text-to-Speech Synthesis

This script demonstrates how to convert text to natural-sounding speech using
OpenAI's TTS (Text-to-Speech) API. It supports multiple voices and speech models.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Convert text to natural-sounding speech
    - Support for multiple voice options
    - Adjustable speech parameters (speed, pitch)
    - Save audio output to MP3 files

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python text_to_speech.py
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
