"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

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

output = client.chat.completions.create(
    model=MODEL,
    messages=messages
)

print(output)
