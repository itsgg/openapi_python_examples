"""
This is a simple example of how to use the YouTube transcript API.
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


transcript = YouTubeTranscriptApi.get_transcript(video_id)
FULL_TEXT = " ".join([entry["text"] for entry in transcript])
text_chunks = chunk_text(FULL_TEXT)

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
        time.sleep(1)  # Rate limit handling
    except RateLimitError:
        print("Rate limit hit, waiting 60 seconds...")
        time.sleep(60)
        continue

print("\nFinal Summary:")
print("\n".join(summaries))
