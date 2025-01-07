"""
This is a simple example of how to use the OpenAI API wrapper.
"""

import os
from typing import List

from openai import OpenAI

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def ask_chatgpt(messages):
    """
    Ask ChatGPT a question and return the answer.

    Args:
        messages (list): A list of messages to send to the chatbot.

    Returns:
        str: The answer from the chatbot.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content


PROMPT_ROLE = """
You are an assistant for journalists. Your task is to write articles, based on the FACTS that are given to you. 
You should respect the instructions: the TONE, LENGTH and STYLE.
"""


def assist_journalist(
    facts: List[str], tone: str, length_words: int, style: str
) -> str:
    """
    Assist a journalist in writing a news article.
    """

    facts = ", ".join(facts)
    prompt = f"{PROMPT_ROLE} \
     FACTS: {facts} \
     TONE: {tone} \
     LENGTH: {length_words} \
     STYLE: {style} \
    "

    return ask_chatgpt([{"role": "user", "content": prompt}])


print(
    assist_journalist(
        ["Mindfulness is easy", "Mindfulness helps with stress, anxiety & depression"],
        "informative",
        100,
        "formal",
    )
)
