import os
import subprocess
import random
from io import BytesIO
import tempfile
import time
from clients.deepgram import DeepgramService

deepgram_service = DeepgramService()

def get_audio_duration(file_path: str) -> float:
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.stderr:
            print(f"FFprobe stderr: {result.stderr.decode()}")
        duration_str = result.stdout.decode().strip()
        return float(duration_str) if duration_str else 0.0
    except Exception as e:
        print(f"Exception in get_audio_duration: {e}")
        return 0.0


def get_video_duration(file_path: str) -> float:
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        duration_str = result.stdout.decode().strip()
        return float(duration_str) if duration_str else 0.0
    except Exception as e:
        print(f"Exception in get_video_duration: {e}")
        return 0.0


def process_video_streaming(audio_bytes: BytesIO, video_bytes: BytesIO) -> bytes:
    """
    Combines video with audio file using streaming pipeline
    """
    start_time = time.time()
    print("Starting video processing pipeline")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Centralize file creation
        temp_audio_path = os.path.join(tmpdir, "audio.wav")
        temp_video_path = os.path.join(tmpdir, "video.mp4")
        srt_file_path = os.path.join(tmpdir, "captions.srt")
        ass_file_path = os.path.join(tmpdir, "subtitles.ass")

        # Write input bytes to files
        audio_bytes.seek(0)
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes.read())

        video_bytes.seek(0)
        with open(temp_video_path, "wb") as f:
            f.write(video_bytes.read())

        # Use centralized files for duration check
        video_duration = get_video_duration(temp_video_path)
        audio_duration = get_audio_duration(temp_audio_path)

        print(f"Duration calculation took {time.time() - start_time:.2f} seconds")
        if audio_duration >= video_duration:
            raise ValueError(f"Audio duration ({audio_duration}s) >= video duration ({video_duration}s)")

        # Calculate random start time
        max_start_time = video_duration - audio_duration
        print('The audio duration is ', audio_duration)
        print('The video duration is ', video_duration)
        start_time = round(random.uniform(0, max_start_time), 2)
        print(f"Starting at {start_time}s with {audio_duration}s segment")

        # Generate captions
        caption_start = time.time()
        captions = deepgram_service.generate_captions_with_deepgram(temp_audio_path)
        print(f"Caption generation took {time.time() - caption_start:.2f} seconds")

        # Convert captions to ASS
        deepgram_service.convert_srt_to_ass(
            srt_captions=captions,
            srt_file_path=srt_file_path,
            ass_file_path=ass_file_path
        )

        # Simplify ASS styling
        with open(ass_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(ass_file_path, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("Style:"):
                    parts = line.strip().split(",")
                    if len(parts) >= 18:
                        parts[1] = "Arial"
                        parts[2] = "13"
                        parts[5] = "&H00000000"
                        parts[16] = "1"
                        parts[17] = "0"
                        line = ",".join(parts) + "\n"
                f.write(line)

        # Run FFmpeg
        ffmpeg_start = time.time()
        ffmpeg_process = subprocess.Popen([
            'ffmpeg',
            '-y',
            '-ss', str(start_time),
            '-i', temp_video_path,
            '-i', temp_audio_path,
            '-vf', f"subtitles={ass_file_path}:force_style='FontName=Arial,FontSize=16,Outline=1,Shadow=0'",
            '-t', str(audio_duration),
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-b:a', '256k',
            '-ar', '48000',
            '-ac', '2',
            '-shortest',
            '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
            '-f', 'mp4',
            'pipe:1'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, stderr = ffmpeg_process.communicate()

        if ffmpeg_process.returncode != 0:
            print(f"FFmpeg failed: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")

        if not output:
            print("FFmpeg produced empty output")
            raise RuntimeError("FFmpeg produced empty output")

        print(f"FFmpeg processing with captions took {time.time() - ffmpeg_start:.2f} seconds")
        return output


