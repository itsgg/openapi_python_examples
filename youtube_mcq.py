"""
YouTube Video Educational Content Processor.

This module processes YouTube video content togenerate educational materials,
specifically multiple choice questions (MCQs) from video transcripts.

Dependencies:
    - youtube_transcript_api
    - openai
    - langchain

Main Features:
    1. Extracts transcripts using the YouTube API
    2. Chunks large transcripts into manageable pieces
    3. Generates concise summaries using OpenAI's GPT-4
    4. Creates multiple choice questions for educational purposes

Example Usage:
    from youtube_mcq import YouTubeMCQGenerator
    
    generator = YouTubeMCQGenerator("video_url")
    mcqs = generator.generate_questions()
    print(mcqs)
"""

import os
import time
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI, RateLimitError

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

YOUTUBE_URL = "https://www.youtube.com/watch?v=P99aw9snZi0"
video_id = YOUTUBE_URL.split("v=")[1]


def chunk_text(text, chunk_size=4000):
    """
    Split text into smaller chunks of specified size.

    Args:
        text (str): The input text to be chunked
        chunk_size (int): Maximum size of each chunk in characters

    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_size += len(word) + 1  # +1 for space
        if current_size > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def generate_mcq_from_summary(summary):
    """
    Generate multiple choice questions from a text summary.

    Args:
        summary (str): Text summary to generate questions from

    Returns:
        str: Generated MCQ questions or None if generation fails
    """
    retries = 3
    for i in range(retries):
        try:
            mcq_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": (
                            "Generate multiple choice questions from the following "
                            f"summary:\n\n{summary}"
                        ),
                    },
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            questions = mcq_response.choices[0].message.content.strip()
            return questions
        except RateLimitError:
            print(f"Rate limit exceeded. Retrying in {2 ** i} seconds...")
            time.sleep(2**i)
    print("Failed to generate MCQs after several retries.")
    return None

def main():
    """Process YouTube video to generate summary and MCQ questions."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_chunks = chunk_text(" ".join([entry["text"] for entry in transcript]))

    summaries = []
    for chunk in text_chunks:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Summarize this text concisely:"},
                    {"role": "user", "content": chunk},
                ],
            )
            summaries.append(response.choices[0].message.content)
            time.sleep(1)
        except RateLimitError:
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            continue

    print("\nFinal Summary:")
    print("\n".join(summaries))

    mcq_questions = generate_mcq_from_summary("\n".join(summaries))
    if mcq_questions:
        print("\nGenerated MCQ Questions:")
        print(mcq_questions)


if __name__ == "__main__":
    main()
