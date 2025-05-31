from fastapi import APIRouter, HTTPException
from ..services.reddit_service import extract_post_and_top_comments
from ..clients.openai_client import generate_commentary_script, text_to_speech_file
from ..clients.s3_client import read_file_from_s3, upload_file_to_s3, get_s3_url
from ..clients.video_client import process_video_streaming
from ..services.task_queue import task_queue, TaskStatus
import os
from dotenv import load_dotenv
import asyncio

router = APIRouter()

load_dotenv()
BUCKET_NAME = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')

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
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_REDDIT_POST, "Fetching Reddit content...")
        post_data = extract_post_and_top_comments(url)
        
        # Step 2: Generate script
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_SCRIPT, "Generating script...")
        script = generate_commentary_script(post_data["title"], post_data["description"])
        
        # Step 3: Generate audio
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_VOICEOVER, "Generating audio...")
        audio_speech = text_to_speech_file(script)
        
        # Step 4: Get video template
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_BACKGROUND_VIDEO, "Preparing video template...")
        subway_surfers_video = read_file_from_s3(BUCKET_NAME, "subway_surfers.mp4")
        
        # Step 5: Process video
        task_queue.update_task_status(task_id, TaskStatus.PROCESSING_VIDEO, "Processing video...")
        video_bytes = process_video_streaming(audio_speech, subway_surfers_video, True)  # Enable captions
        
        # Save video locally
        output_path = f"output_video_{task_id}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_bytes)
        print(f"Video saved to: {output_path}")

        # Step 6: Upload video to S3
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL, "Uploading video to S3...")
        upload_file_to_s3(video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")

        # Step 7: Get S3 URL for the video
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL, "Getting video URL...")
        video_url = get_s3_url(BUCKET_NAME, f"output_video_{task_id}.mp4")
        
        # Update task status to COMPLETED with video URL
        task_queue.update_task_status(task_id, TaskStatus.COMPLETED, video_url=video_url)
    except Exception as e:
        # If an error occurs, mark the task as failed
        task_queue.update_task_status(task_id, TaskStatus.FAILED, error=str(e))

@router.get("/reddit-commentary/status/{task_id}")
def get_task_status(task_id: str):
    task = task_queue.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    response = {
        "status": task["status"].value,
        "error": task.get("error"),
        "message": task.get("message", ""),
        "video_url": task.get("video_url", "")
    }
    print(f"Task status response for {task_id}:", response)
    return response
