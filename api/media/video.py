import os
import subprocess
import random
from io import BytesIO
import tempfile
import time
from clients.deepgram import DeepgramService

deepgram_service = DeepgramService()

def get_audio_duration(audio_bytes: BytesIO) -> float:
    """
    Get the duration of an audio file in seconds.
    """
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes.read())
        tmp.flush()
        tmp_path = tmp.name  # store path before closing

    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration_str = result.stdout.decode().strip()
        return float(duration_str) if duration_str else 0.0
    finally:
        # Ensure the file is removed after we're done
        os.remove(tmp_path)

def get_video_duration(video_bytes: BytesIO) -> float:
    """
    Get the duration of a video file in seconds.
    """
    # Write BytesIO content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_bytes.read())
        temp_file.flush()
        temp_path = temp_file.name

    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', temp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration_str = result.stdout.decode().strip()
        return float(duration_str) if duration_str else 0.0
    finally:
        os.remove(temp_path)

def process_video_streaming(audio_bytes: BytesIO, video_bytes: BytesIO) -> bytes:
    """
    Combines video with audio file using streaming pipeline
    """
    start_time = time.time()
    print("Starting video processing pipeline")
    
    # Get video duration
    video_duration = get_video_duration(video_bytes)
    audio_duration = get_audio_duration(audio_bytes)
    video_bytes.seek(0)
    audio_bytes.seek(0)
    print(f"Duration calculation took {time.time() - start_time:.2f} seconds")
    
    if audio_duration >= video_duration:
        raise ValueError(f"Audio duration ({audio_duration}s) >= video duration ({video_duration}s)")

    # Calculate random start time
    max_start_time = video_duration - audio_duration
    start_time = round(random.uniform(0, max_start_time), 2)
    print(f"Starting at {start_time}s with {audio_duration}s segment")

    caption_start = time.time()
    captions = deepgram_service.generate_captions_with_deepgram(audio_bytes.getvalue())
    audio_bytes.seek(0)
    print(f"Caption generation took {time.time() - caption_start:.2f} seconds")
    
    ass_file_path = ""
    temp_video_path = ""
    temp_audio_path = ""

    try:
        ass_content = deepgram_service.convert_srt_to_ass(captions)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ass") as ass_file:
            ass_file.write(ass_content.encode('utf-8'))
            ass_file.flush()
            ass_file_path = ass_file.name

        # Simplify ASS styling
        with open(ass_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(ass_file_path, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("Style:"):
                    parts = line.strip().split(",")
                    parts[1] = "Arial"
                    parts[2] = "13"
                    parts[5] = "&H00000000"
                    parts[16] = "1"
                    parts[17] = "0"
                    line = ",".join(parts) + "\n"
                f.write(line)

        ffmpeg_start = time.time()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:

            temp_video.write(video_bytes.read())
            temp_audio.write(audio_bytes.read())
            temp_video.flush()
            temp_audio.flush()
            temp_video_path = temp_video.name
            temp_audio_path = temp_audio.name

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

    finally:
        for path in [ass_file_path, temp_video_path, temp_audio_path]:
            if path and os.path.exists(path):
                os.remove(path)
