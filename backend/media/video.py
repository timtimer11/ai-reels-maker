import os
import tempfile
from io import BytesIO
from moviepy import VideoFileClip, AudioFileClip, TextClip
from clients.deepgram import DeepgramService
import subprocess

deepgram_service = DeepgramService()

def get_audio_duration(file_path: str) -> float:
    """Return the duration of an audio file in seconds"""
    return AudioFileClip(file_path).duration

def get_video_duration(file_path: str) -> float:
    """Return the duration of a video file in seconds"""
    return VideoFileClip(file_path).duration

def subtitle_generator(txt: str) -> TextClip:
    """Generate a TextClip for subtitles."""
    return TextClip(text=txt, font_size=24, color='white', stroke_color='black', stroke_width=1)

def process_video_streaming(audio_bytes: bytes, video_bytes: BytesIO) -> BytesIO:
    """
    Merge video, audio, and captions with length check using MoviePy
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write input bytes to temp files
        audio_path = os.path.join(tmpdir, "audio.wav")
        video_path = os.path.join(tmpdir, "video.mp4")
        srt_path   = os.path.join(tmpdir, "captions.srt")
        output_path= os.path.join(tmpdir, "output.mp4")

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        video_bytes.seek(0)
        with open(video_path, "wb") as f:
            f.write(video_bytes.read())

        # Generate and write captions (SRT)
        srt_content = deepgram_service.generate_captions_with_deepgram(audio_path)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-stream_loop', '-1',  # Loop video to match audio length
            '-i', video_path,
            '-i', audio_path,
            '-vf', f"subtitles='{srt_path}':force_style='Fontsize=18'",  # Burn subtitles
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '28',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-map', '0:v',  # Map video from first input
            '-map', '1:a',  # Map audio from second input
            '-shortest',  # End with shortest stream
            output_path
        ]
        # Execute FFmpeg
        try:
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE, timeout=300)
            # Verify and return output
            with open(output_path, "rb") as f:
                if f.read(1):  # Check not empty
                    f.seek(0)
                    return BytesIO(f.read())
                raise RuntimeError("Empty output file")
        except subprocess.CalledProcessError:
            raise RuntimeError("Video processing failed")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Processing timed out after 5 minutes")