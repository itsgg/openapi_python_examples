"""
OpenAI Speech-to-Text Transcription

This script demonstrates how to use OpenAI's Whisper API to convert audio files into text.
It provides a simple interface for transcribing speech from various audio formats.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Transcribe audio files to text using OpenAI's Whisper model
    - Support for multiple audio formats (MP3, WAV, etc.)
    - Handles API authentication and error responses

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python speech_to_text.py
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

with open("output.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(transcript.text)
