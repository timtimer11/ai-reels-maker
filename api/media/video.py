import subprocess
import random
from io import BytesIO
import tempfile
import logging
import time
import os
from ..clients.deepgram import DeepgramService

# Set up logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'generation_logs.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

deepgram_service = DeepgramService()

def get_audio_duration(audio_bytes: BytesIO) -> float:
    """
    Get the duration of an audio file in seconds.
    """
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
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
    """
    Get the duration of a video file in seconds.
    """
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

def process_video_streaming(audio_bytes: BytesIO, video_bytes: BytesIO) -> bytes:
    """
    Combines video with audio file using streaming pipeline
    """
    start_time = time.time()
    logging.info("Starting video processing pipeline")
    
    # Get video duration
    video_duration = get_video_duration(video_bytes)
    audio_duration = get_audio_duration(audio_bytes)
    video_bytes.seek(0)
    audio_bytes.seek(0)
    logging.info(f"Duration calculation took {time.time() - start_time:.2f} seconds")
    
    if audio_duration >= video_duration:
        raise ValueError(f"Audio duration ({audio_duration}s) >= video duration ({video_duration}s)")

    # Calculate random start time
    max_start_time = video_duration - audio_duration
    start_time = round(random.uniform(0, max_start_time), 2)
    logging.info(f"Starting at {start_time}s with {audio_duration}s segment")

    caption_start = time.time()
    # Generate captions first
    captions = deepgram_service.generate_captions_with_deepgram(audio_bytes.getvalue())
    audio_bytes.seek(0)  # Reset audio position after caption generation
    logging.info(f"Caption generation took {time.time() - caption_start:.2f} seconds")
    
    # Convert SRT to ASS and get the content
    ass_content = deepgram_service.convert_srt_to_ass(captions)
    
    # Create a temporary file for the ASS content
    with tempfile.NamedTemporaryFile(delete=True, suffix=".ass") as ass_file:
        # Write the ASS content to the temporary file
        ass_file.write(ass_content.encode('utf-8'))
        ass_file.flush()
        
        # Simplified ASS styling
        with open(ass_file.name, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        with open(ass_file.name, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("Style:"):
                    parts = line.strip().split(",")
                    parts[1] = "Arial"  # Simpler font
                    parts[2] = "13"     # Larger font size
                    parts[5] = "&H00000000"  # Transparent outline
                    parts[16] = "1"     # Simpler outline
                    parts[17] = "0"     # No shadow
                    line = ",".join(parts) + "\n"
                f.write(line)
        
        # Process video with captions
        ffmpeg_start = time.time()
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video, \
                tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
            
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
                '-b:a', '256k',  # Increased bitrate for WAV conversion
                '-ar', '48000',
                '-ac', '2',
                '-shortest',
                '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
                '-f', 'mp4',
                'pipe:1'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            output, stderr = ffmpeg_process.communicate()
            
            if ffmpeg_process.returncode != 0:
                logging.error(f"FFmpeg failed: {stderr.decode()}")
                raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
                
            if not output:
                logging.error("FFmpeg produced empty output")
                raise RuntimeError("FFmpeg produced empty output")

            logging.info(f"FFmpeg processing with captions took {time.time() - ffmpeg_start:.2f} seconds")
            return output