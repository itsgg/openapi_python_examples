"""
OpenAI Vision API Image Analysis

This script demonstrates how to use OpenAI's GPT-4 Vision API to analyze and
understand images. It can describe images, answer questions about them, and
extract information from visual content.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Analyze and describe images using GPT-4 Vision
    - Support for both image URLs and local files
    - Multiple analysis modes (description, detail extraction)
    - Handle various image formats (PNG, JPEG, etc.)

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python vision.py
"""

import os
from openai import OpenAI, OpenAIError

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"
IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/f/f0/Ophiopteris_antipodum.JPG"
)
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Give the name of the animal in the image"},
            {
                "type": "image_url",
                "image_url": {"url": IMAGE_URL},
            },
        ],
    }
]

try:
    if not client.api_key:
        raise ValueError("OpenAI API key not found in environment variables")

    response = client.chat.completions.create(model=MODEL, messages=messages)

except OpenAIError as e:
    print(f"OpenAI API error occurred: {str(e)}")
except ValueError as e:
    print(f"Configuration error: {str(e)}")

print(response.choices[0].message.content)
