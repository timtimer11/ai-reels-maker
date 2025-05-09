
import whisper
import io
from typing import Tuple

# Load Whisper once globally (use turbo if you've fine-tuned or patched it)
model = whisper.load_model("turbo")  

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
