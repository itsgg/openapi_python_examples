"""
OpenAI Text Embeddings Generator

This script demonstrates how to generate vector embeddings from text using
OpenAI's embedding models. These embeddings can be used for semantic search,
text similarity, and other NLP tasks.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Generate vector embeddings from text input
    - Support for different embedding models
    - Batch processing of multiple texts
    - Optimized for semantic search applications

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python embeddings.py
"""

import os
from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

result = client.embeddings.create(
    input="The food was delicious and the waiter...", model="text-embedding-3-small"
)

print(result)
