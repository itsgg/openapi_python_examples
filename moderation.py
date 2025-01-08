"""
OpenAI Content Moderation

This script demonstrates how to use OpenAI's moderation API to detect and filter
potentially harmful or inappropriate content. It helps ensure content safety
and compliance with content guidelines.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Detect potentially harmful content
    - Check for various content categories (violence, hate, etc.)
    - Real-time content moderation
    - Batch processing of multiple texts

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python moderation.py
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.moderations.create(
    model="omni-moderation-latest", input="I want to kill my neighbour."
)

print(response.results[0])
