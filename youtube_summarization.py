"""
YouTube Video Summarization Module

This module provides functionality to extract and summarize YouTube video transcripts
using the YouTube Transcript API and OpenAI's language models.

Dependencies:
    - youtube_transcript_api
    - openai
    - os
    - time

Main Features:
    - Extract transcripts from YouTube videos
    - Generate AI-powered summaries of video content
    - Handle rate limiting and API errors

Example Usage:
    from youtube_summarization import summarize_video
    
    video_id = "dQw4w9WgXcQ"
    summary = summarize_video(video_id)
    print(summary)
"""

import os
import time
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from openai import OpenAI, OpenAIError, RateLimitError

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def extract_video_id(url: str) -> str:
    """
    Extract video ID from a YouTube URL.

    Args:
        url (str): YouTube video URL

    Returns:
        str: YouTube video ID

    Raises:
        ValueError: If URL format is invalid
    """
    try:
        if "v=" not in url:
            raise ValueError("Invalid YouTube URL format")
        return url.split("v=")[1].split("&")[0]
    except Exception as e:
        raise ValueError(f"Failed to extract video ID: {str(e)}")


def chunk_text(text: str, chunk_size: int = 4000) -> List[str]:
    """
    Split text into smaller chunks of specified size.

    Args:
        text (str): The input text to be chunked
        chunk_size (int): Maximum size of each chunk in characters

    Returns:
        List[str]: List of text chunks
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


def summarize_text(text: str, model: str = "gpt-4") -> str:
    """
    Generate a summary of the given text using OpenAI's API.

    Args:
        text (str): Text to summarize
        model (str): OpenAI model to use

    Returns:
        str: Generated summary

    Raises:
        OpenAIError: If API call fails
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Summarize this text concisely:"},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content
    except RateLimitError:
        print("Rate limit hit, waiting 60 seconds...")
        time.sleep(60)
        return summarize_text(text, model)  # Retry
    except OpenAIError as e:
        raise OpenAIError(f"Failed to generate summary: {str(e)}")


def main():
    """Main function to process YouTube video and generate summary."""
    try:
        if not client.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        YOUTUBE_URL = "https://www.youtube.com/watch?v=P99aw9snZi0"
        video_id = extract_video_id(YOUTUBE_URL)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video")
            return
        except Exception as e:
            print(f"Failed to fetch transcript: {str(e)}")
            return

        FULL_TEXT = " ".join([entry["text"] for entry in transcript])
        text_chunks = chunk_text(FULL_TEXT)

        summaries = []
        for chunk in text_chunks:
            summary = summarize_text(chunk)
            if summary:
                summaries.append(summary)

        print("\nFinal Summary:")
        print("\n".join(summaries))

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
