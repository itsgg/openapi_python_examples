"""
OpenAI Image Editing API Integration

This script demonstrates how to use OpenAI's DALL-E API for image editing and manipulation.
It allows you to edit existing images by providing natural language prompts.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Edit existing images using natural language prompts
    - Support for various image formats (PNG, JPEG)
    - Handles API authentication and error responses

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python image_edit.py
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

with open("output.png", "rb") as image_file, open("mask.png", "rb") as mask_file:
    response = client.images.edit(
        image=image_file,
        mask=mask_file,
        prompt="A indian man is walking down the street.",
    )

print(response.data[0].url)
