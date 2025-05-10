import whisper
from io import BytesIO
from typing import Tuple
import tempfile

# Load model once globally
model = whisper.load_model("turbo")

def generate_captions_from_audio(audio_bytes: BytesIO) -> Tuple[str, list]:
    """
    Transcribes audio bytes using Whisper and returns the raw transcript and SRT content.
    """
    # Save BytesIO to temp file because whisper expects a file path
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp:
        tmp.write(audio_bytes.read())
        tmp.flush()  # ensure it's written

        result = model.transcribe(tmp.name)
        transcript = result["text"]
        segments = result["segments"]

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
