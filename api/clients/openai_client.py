import os
from openai import OpenAI
import whisper
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_commentary_script(title: str, description: str) -> str:
    prompt = f"""
        Generate a concise, engaging voiceover script for vertical Shorts video:

        Title: {title}
        Description: {description}

        Follow these rules exactly:
        1. Respond ONLY with the voiceover text. Do NOT include any commentary, explanations, or formatting markup.
        2. Use clear, simple language suitable for a broad audience.
        3. Avoid special characters or emojis.
        4. Do not include profanity, slurs, or any NSFW content.
        5. Do NOT start with a greeting.
        6. Structure the script as:
        • Hook: 1–2 sentences to grab attention immediately.
        • Story: unfold the narrative or key points.
        • Payoff: 1–2 sentences delivering a satisfying conclusion.
        • Start with something like: "Did you know", or catchy line
    """
    print('generating commentary script with openai api')
    openai_response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    print('done on commentary script with openai api')
    return openai_response.output_text

def text_to_speech_file(text: str, voice: str = "onyx") -> bytes:
    try:
        # Generate speech using OpenAI TTS API
        response = openai_client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            speed=3,
            response_format='mp3',
            input=text,
            instructions="Speak in a insightful and excited tone."
        )

        audio_data = BytesIO(response.content)
        return audio_data
    except Exception as e:
        print(f"Error generating speech: {e}")
        raise e

import whisper
import io
from typing import Tuple

# Load Whisper once globally (use turbo if you've fine-tuned or patched it)
model = whisper.load_model("base")  # or "small", "medium", etc.

def generate_captions_from_audio(audio_bytes: bytes) -> Tuple[str, list]:
    """
    Transcribes audio bytes using Whisper and returns the raw transcript and SRT content.
    """
    # Treat bytes as a file-like object
    audio_file = io.BytesIO(audio_bytes)

    # Transcribe using Whisper
    result = model.transcribe(audio_file)
    transcript = result["text"]
    segments = result["segments"]

    # Convert segments to SRT format
    def format_time(seconds: float) -> str:
        ms = int((seconds - int(seconds)) * 1000)
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    srt_lines = []
    for i, segment in enumerate(segments, start=1):
        start = format_time(segment["start"])
        end = format_time(segment["end"])
        text = segment["text"].strip()
        srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n")

    srt_content = "\n".join(srt_lines)

    return transcript, srt_content.splitlines()
