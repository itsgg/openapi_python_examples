"""
This is a simple example of how to use the OpenAI API wrapper.
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
