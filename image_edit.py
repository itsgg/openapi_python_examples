"""
This is a simple example of how to use the OpenAI API wrapper.
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
