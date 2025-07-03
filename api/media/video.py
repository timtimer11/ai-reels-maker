import os
import tempfile
from io import BytesIO
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from clients.deepgram import DeepgramService

deepgram_service = DeepgramService()

def get_audio_duration(file_path: str) -> float:
    """Return the duration of an audio file in seconds."""
    return AudioFileClip(file_path).duration


def get_video_duration(file_path: str) -> float:
    """Return the duration of a video file in seconds."""
    return VideoFileClip(file_path).duration


def subtitle_generator(txt: str) -> TextClip:
    """Generate a TextClip for subtitles."""
    return TextClip(txt, font='Arial', fontsize=24)


def process_video_streaming(audio_bytes: bytes, video_bytes: BytesIO) -> bytes:
    """
    Merge video, audio, and captions with length check using MoviePy.
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

        # Duration checks
        a_duration = get_audio_duration(audio_path)
        v_duration = get_video_duration(video_path)
        if a_duration >= v_duration:
            raise ValueError(f"Audio duration ({a_duration:.2f}s) >= video duration ({v_duration:.2f}s)")

        # Load clips
        audio_clip = AudioFileClip(audio_path)
        video_clip = VideoFileClip(video_path).with_audio(audio_clip)

        # Generate and write captions (SRT)
        srt_content = deepgram_service.generate_captions_with_deepgram(audio_path)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        # Create subtitles overlay
        subtitles = SubtitlesClip(
            srt_path,
            make_textclip=subtitle_generator,
            encoding='utf-8'
        ).set_position(('center', 'bottom'))

        # Compose final clip
        final = CompositeVideoClip([video_clip, subtitles])

        # Export
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

        # Read result
        with open(output_path, "rb") as f:
            return f.read()