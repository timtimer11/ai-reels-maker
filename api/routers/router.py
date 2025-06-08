from fastapi import APIRouter, HTTPException
from ..services.reddit_service import extract_post_and_top_comments
from ..clients.openai_client import generate_commentary_script, text_to_speech_file
from ..clients.s3_client import read_file_from_s3, upload_file_to_s3, get_s3_url
from ..clients.video_client import process_video_streaming
from ..services.task_queue import task_queue, TaskStatus
import os
from dotenv import load_dotenv
import asyncio
import time
from datetime import datetime

router = APIRouter()

load_dotenv()
BUCKET_NAME = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')

def log_timing(task_id: str, step: str, start_time: float):
    """Log timing information to a file"""
    end_time = time.time()
    duration = end_time - start_time
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"task_{task_id}_timing.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {step}: {duration:.2f} seconds\n")

@router.post("/reddit-commentary")
async def start_reddit_commentary(url: str):
    # Create task and set status to PROCESSING
    task_id = task_queue.create_task()
    task_queue.update_task_status(task_id, TaskStatus.PROCESSING)
    
    # Start processing in background
    asyncio.create_task(process_reddit_commentary(task_id, url))
    
    return {"task_id": task_id}

async def process_reddit_commentary(task_id: str, url: str):
    try:
        # Step 1: Get Reddit content
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_REDDIT_POST, "Fetching Reddit content...")
        post_data = extract_post_and_top_comments(url)
        log_timing(task_id, "Fetch Reddit Content", start_time)
        
        # Step 2: Generate script
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_SCRIPT, "Generating script...")
        script = generate_commentary_script(post_data["title"], post_data["description"])
        log_timing(task_id, "Generate Script", start_time)
        
        # Step 3: Generate audio
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_VOICEOVER, "Generating audio...")
        audio_speech = text_to_speech_file(script)
        log_timing(task_id, "Generate Audio", start_time)
        
        # Step 4: Get video template
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_BACKGROUND_VIDEO, "Preparing video template...")
        subway_surfers_video = read_file_from_s3(BUCKET_NAME, "subway_surfers_short.mp4")
        log_timing(task_id, "Fetch Video Template", start_time)
        
        # Step 5: Process video
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.PROCESSING_VIDEO, "Processing video...")
        video_bytes = process_video_streaming(audio_speech, subway_surfers_video, True)  # Enable captions
        log_timing(task_id, "Process Video", start_time)
        
        # Save video locally
        output_path = f"output_video_{task_id}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_bytes)
        print(f"Video saved to: {output_path}")

        # Step 6: Upload video to S3
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL, "Uploading video to S3...")
        upload_file_to_s3(video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")
        log_timing(task_id, "Upload to S3", start_time)

        # Step 7: Get S3 URL for the video
        start_time = time.time()
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL, "Getting video URL...")
        video_url = get_s3_url(BUCKET_NAME, f"output_video_{task_id}.mp4")
        log_timing(task_id, "Get Video URL", start_time)
        
        # Update task status to COMPLETED with video URL
        task_queue.update_task_status(task_id, TaskStatus.COMPLETED, video_url=video_url)
        
        # Log total time
        log_timing(task_id, "Total Processing Time", time.time() - start_time)
    except Exception as e:
        # If an error occurs, mark the task as failed
        task_queue.update_task_status(task_id, TaskStatus.FAILED, error=str(e))
        log_timing(task_id, f"Failed with error: {str(e)}", time.time() - start_time)

@router.get("/reddit-commentary/status/{task_id}")
def get_task_status(task_id: str):
    task = task_queue.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    response = {
        "status": task["status"].value,
        "error": task.get("error"),
        "video_url": task.get("video_url", "")
    }
    print(f"Task status response for {task_id}:", response)
    return response
