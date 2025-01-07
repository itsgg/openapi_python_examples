"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
response_format = {"type", "text"}

# MODEL = "gpt-3.5-turbo"
# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "What is the purpose of life?"},
# ]

# MODEL = "chatgpt-4o-latest"
# IMAGE_URL = (
#     "https://upload.wikimedia.org/wikipedia/commons/f/f0/Ophiopteris_antipodum.JPG"
# )
# messages = [
#     {
#         "role": "user",
#         "content": [
#             {"type": "text", "text": "Give the name of the animal in the image"},
#             {
#                 "type": "image_url",
#                 "image_url": {"url": IMAGE_URL},
#             },
#         ],
#     }
# ]

MODEL = "chatgpt-4o-latest"
messages = [
    {
        "role": "system",
        "content": "Convert the response to JSON",
    },
    {
        "role": "user",
        "content": "List the hierarchy of human species.",
    },
]
response_format = {"type": "json_object"}

output = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    response_format=response_format,
)

print(output)
