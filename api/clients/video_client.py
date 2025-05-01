import subprocess
import os
import random
from dotenv import load_dotenv
from io import BytesIO
from s3_client import upload_audio_to_s3,read_file_from_s3
from openai_client import text_to_speech_file
import tempfile

load_dotenv()

BUCKET_NAME = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')

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

def process_video_streaming(audio_bytes: BytesIO, video_bytes: BytesIO) -> bytes:
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

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video, \
         tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
         # Ensure BytesIO is at start
       
        # Write to temp files
        temp_video.write(video_bytes.read())
        temp_audio.write(audio_bytes.read())
        temp_video.flush()
        temp_audio.flush()
    
        # Calculate random start time
        max_start_time = video_duration - audio_duration
        start_time = round(random.uniform(0, max_start_time), 2)
        print(f"Starting at {start_time}s with {audio_duration}s segment")

        ffmpeg_process = subprocess.Popen([
            'ffmpeg',
            '-y',
            '-ss', str(start_time),          # start offset
            '-i', temp_video.name,                # video input
            '-i', temp_audio.name,                # audio input
            '-t', str(audio_duration),       # duration to mux
            '-map', '0:v:0',                 # video stream
            '-map', '1:a:0',                 # audio stream
            '-c:v', 'copy',                  # copy video codec
            '-c:a', 'aac',                   # encode audio to AAC
            '-b:a', '192k',                  # ↑ bump audio bitrate
            '-ar', '48000',                  # ↑ sample rate
            '-ac', '2',                      # ↑ stereo
            '-shortest',                     # match shortest stream
            '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
            '-f', 'mp4',                     # fragmented MP4 for pipe
            'pipe:1'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output, stderr = ffmpeg_process.communicate()
        
        if ffmpeg_process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
            
        if not output:
            raise RuntimeError("FFmpeg produced empty output")
            
        return output

if __name__ == "__main__":
    audio_speech = text_to_speech_file(text="this is a test audio script for money making idea")
    subway_surfers_video = read_file_from_s3(bucket_name=BUCKET_NAME, file_name="subway_surfers.mp4")
    # video_length = get_video_duration(subway_surfers_video)
    # print(video_length)
    # with open("test.mp3", "wb") as f:
    #     f.write(obj.getbuffer())
    combined_video_audio = process_video_streaming(audio_speech, subway_surfers_video)
    # save the video to a file
    with open("final+v.mp4", "wb") as f:
        f.write(combined_video_audio)
    # video_buffer = BytesIO(result)
    # output_path = f"output_{random.randint(1000, 9999)}.mp4"
    # s3_url = upload_audio_to_s3(object_name=video_buffer, bucket_name=BUCKET_NAME, file_name_in_s3=output_path)