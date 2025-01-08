"""
News Generator Module

This module generates news articles and summaries using OpenAI's API.
It provides functionality to create articles based on given facts and style preferences.

Dependencies:
    - openai: OpenAI API client library
    - Environment variable OPENAI_API_KEY must be set

Features:
    - Generates news articles based on given facts
    - Customizable tone and style
    - Error handling and rate limiting
    - Type-safe interfaces

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python news_generator.py
"""

import os

from typing import List, Dict
from openai import OpenAI, OpenAIError

# Initialize OpenAI client
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_ROLE = """
You are an assistant for journalists. Your task is to write articles, based on the FACTS that are given to you. 
You should respect the instructions: the TONE, LENGTH and STYLE.
"""


def ask_chatgpt(messages: List[Dict[str, str]], model: str = "gpt-4") -> str:
    """
    Send a request to ChatGPT and get the response.

    Args:
        messages (List[Dict[str, str]]): List of message dictionaries for the conversation
        model (str): OpenAI model to use

    Returns:
        str: The response content from ChatGPT

    Raises:
        OpenAIError: If API call fails
        ValueError: If API key is not set
    """
    if not client.api_key:
        raise ValueError("OpenAI API key not found in environment variables")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        raise OpenAIError(f"Failed to get response from ChatGPT: {str(e)}") from e


def assist_journalist(
    facts: List[str],
    tone: str,
    length_words: int,
    style: str,
    model: str = "gpt-4",
) -> str:
    """
    Generate a news article based on provided facts and style preferences.

    Args:
        facts (List[str]): List of factual statements to include
        tone (str): Desired tone of the article (e.g., "informative", "casual")
        length_words (int): Target word count
        style (str): Writing style to use (e.g., "formal", "conversational")
        model (str): OpenAI model to use

    Returns:
        str: Generated news article

    Raises:
        ValueError: If input parameters are invalid
        OpenAIError: If API call fails
    """
    if not facts:
        raise ValueError("At least one fact must be provided")
    if length_words <= 0:
        raise ValueError("Length must be a positive number")

    try:
        facts_str = ", ".join(facts)
        prompt = f"{PROMPT_ROLE} \
         FACTS: {facts_str} \
         TONE: {tone} \
         LENGTH: {length_words} \
         STYLE: {style} \
        "

        return ask_chatgpt([{"role": "user", "content": prompt}], model)
    except (ValueError, OpenAIError):
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to generate article: {str(e)}") from e


def main():
    """Main function to demonstrate article generation."""
    try:
        article = assist_journalist(
            facts=[
                "Mindfulness is easy",
                "Mindfulness helps with stress, anxiety & depression"
            ],
            tone="informative",
            length_words=100,
            style="formal",
        )
        print("\nGenerated Article:")
        print(article)

    except (ValueError, OpenAIError, RuntimeError) as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
