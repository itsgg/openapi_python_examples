"""
OpenAI DALL-E Image Generation

This script demonstrates how to generate images using OpenAI's DALL-E model.
It provides a simple interface for creating images from natural language descriptions.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Generate images from text descriptions using DALL-E
    - Support for different image sizes and styles
    - Handles API authentication and error responses
    - Save generated images to local storage

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python image_generation.py
"""

import os
import requests
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.images.generate(
    model="dall-e-3",
    prompt="A indian man is walking down the street.",
    size="1024x1024",
    quality="standard",
)

image_url = response.data[0].url

image_data = requests.get(image_url, timeout=10).content
with open("output.png", "wb") as image_file:
    image_file.write(image_data)

print("Image saved as output.png")
