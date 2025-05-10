import subprocess
import random
from io import BytesIO
import tempfile
from ..clients.captions_client import generate_captions_from_audio

def get_audio_duration(audio_bytes: BytesIO) -> float:
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp:
        tmp.write(audio_bytes.read())
        tmp.flush()

        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', tmp.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration_str = result.stdout.decode().strip()
        print(f"Duration: {duration_str} seconds")
        return float(duration_str) if duration_str else 0.0

def get_video_duration(video_bytes: BytesIO) -> float:
    # Write BytesIO content to a temporary file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_file:
        temp_file.write(video_bytes.read())
        temp_file.flush()  # Ensure data is written before subprocess reads it

        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', temp_file.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return float(result.stdout)

def process_video_streaming(audio_bytes: BytesIO, video_bytes: BytesIO, with_captions=False) -> bytes:
    """
    Combines video with audio file using streaming pipeline
    """
    # Get video duration
    video_duration = get_video_duration(video_bytes)
    audio_duration = get_audio_duration(audio_bytes)
    print(f"Video duration: {video_duration} seconds")
    print(f"Audio duration: {audio_duration} seconds")
    video_bytes.seek(0)
    audio_bytes.seek(0)
    if audio_duration >= video_duration:
        raise ValueError(f"Audio duration ({audio_duration}s) >= video duration ({video_duration}s)")

    # Calculate random start time
    max_start_time = video_duration - audio_duration
    start_time = round(random.uniform(0, max_start_time), 2)
    print(f"Starting at {start_time}s with {audio_duration}s segment")

    if with_captions:
        # Generate captions first
        transcript, captions = generate_captions_from_audio(audio_bytes)
        audio_bytes.seek(0)  # Reset audio position after caption generation
        
        # Write SRT captions to a temp file
        with tempfile.NamedTemporaryFile(delete=True, suffix=".srt") as srt_file:
            captions_text = '\n'.join(captions) if isinstance(captions, list) else str(captions)
            srt_file.write(captions_text.encode())
            srt_file.flush()
            
            # Convert SRT to ASS with simplified styling
            with tempfile.NamedTemporaryFile(delete=True, suffix=".ass") as ass_file:
                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", srt_file.name,
                    ass_file.name
                ], check=True)
                
                # Simplified ASS styling
                with open(ass_file.name, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                with open(ass_file.name, "w", encoding="utf-8") as f:
                    for line in lines:
                        if line.startswith("Style:"):
                            parts = line.strip().split(",")
                            parts[1] = "Arial"  # Simpler font
                            parts[2] = "16"     # Larger font size
                            parts[5] = "&H00000000"  # Transparent outline
                            parts[16] = "1"     # Simpler outline
                            parts[17] = "0"     # No shadow
                            line = ",".join(parts) + "\n"
                        f.write(line)
                
                # Process video with captions
                with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video, \
                     tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
                    
                    temp_video.write(video_bytes.read())
                    temp_audio.write(audio_bytes.read())
                    temp_video.flush()
                    temp_audio.flush()

                    # Optimized FFmpeg command for caption processing
                    ffmpeg_process = subprocess.Popen([
                        'ffmpeg',
                        '-y',
                        '-ss', str(start_time),
                        '-i', temp_video.name,
                        '-i', temp_audio.name,
                        '-vf', f'subtitles={ass_file.name}:force_style=\'FontName=Arial,FontSize=16,Outline=1,Shadow=0\'',
                        '-t', str(audio_duration),
                        '-map', '0:v:0',
                        '-map', '1:a:0',
                        '-c:v', 'libx264',
                        '-preset', 'ultrafast',  # Faster encoding
                        '-c:a', 'aac',
                        '-b:a', '192k',
                        '-ar', '48000',
                        '-ac', '2',
                        '-shortest',
                        '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
                        '-f', 'mp4',
                        'pipe:1'
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    output, stderr = ffmpeg_process.communicate()
                    
                    if ffmpeg_process.returncode != 0:
                        raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
                        
                    if not output:
                        raise RuntimeError("FFmpeg produced empty output")

                    return output
    else:
        # Process video without captions
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video, \
             tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
             
            temp_video.write(video_bytes.read())
            temp_audio.write(audio_bytes.read())
            temp_video.flush()
            temp_audio.flush()

            ffmpeg_process = subprocess.Popen([
                'ffmpeg',
                '-y',
                '-ss', str(start_time),
                '-i', temp_video.name,
                '-i', temp_audio.name,
                '-t', str(audio_duration),
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-ar', '48000',
                '-ac', '2',
                '-shortest',
                '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
                '-f', 'mp4',
                'pipe:1'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            output, stderr = ffmpeg_process.communicate()
            
            if ffmpeg_process.returncode != 0:
                raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
                
            if not output:
                raise RuntimeError("FFmpeg produced empty output")

            return output
