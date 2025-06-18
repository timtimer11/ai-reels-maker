from fastapi import APIRouter
from ..clients.openai import generate_commentary_script, text_to_speech_file
from ..storage.cloudflare_s3 import CloudflareS3
from ..media.video import process_video_streaming
from ..utils.task_queue import task_queue, TaskStatus
from ..clients.reddit import RedditClient
import os
from dotenv import load_dotenv
import asyncio

router = APIRouter()

load_dotenv()
BUCKET_NAME = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')

cloudflare_s3 = CloudflareS3()

@router.post("/reddit-commentary")
async def start_reddit_commentary(url: str):
    task_id = task_queue.create_media_processing_task()
    task_queue.update_task_status(task_id, TaskStatus.PROCESSING)
    
    # Start processing in background
    asyncio.create_task(process_reddit_commentary(task_id, url))
    
    return {"task_id": task_id}

async def process_reddit_commentary(task_id: str, url: str):
    try:
        # Step 1: Get Reddit content
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_REDDIT_POST)
        reddit_client = RedditClient()
        fetched_post = await asyncio.to_thread(reddit_client.fetch_post, url)
        post_data = await asyncio.to_thread(reddit_client.extract_post_data, fetched_post)
        
        # Step 2: Generate script
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_SCRIPT)
        script = await asyncio.to_thread(generate_commentary_script, post_data["title"], post_data["description"])
        
        # Step 3: Generate audio
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_VOICEOVER)
        audio_speech = await asyncio.to_thread(text_to_speech_file, script)
        
        # Step 4: Get video template
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_BACKGROUND_VIDEO)
        subway_surfers_video = await asyncio.to_thread(cloudflare_s3.read_file_from_s3, BUCKET_NAME, "subway_surfers_short.mp4")
        
        # Step 5: Process video
        task_queue.update_task_status(task_id, TaskStatus.PROCESSING_VIDEO)
        video_bytes = await asyncio.to_thread(process_video_streaming, audio_speech, subway_surfers_video)
        
        # Save video locally
        output_path = f"output_video_{task_id}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_bytes)
        print(f"Video saved to: {output_path}")

        # Step 6: Upload video to S3
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL)
        await asyncio.to_thread(cloudflare_s3.upload_file_to_s3, video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")

        # Step 7: Get S3 URL for the video
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL)
        video_url = await asyncio.to_thread(cloudflare_s3.get_s3_url, BUCKET_NAME, f"output_video_{task_id}.mp4")
        
        # Update task status to COMPLETED with video URL
        task_queue.update_task_status(task_id, TaskStatus.COMPLETED, video_url)
        
        # Log total time
    except Exception as e:
        # If an error occurs, mark the task as failed
        task_queue.update_task_status(task_id, TaskStatus.FAILED)
        raise e

@router.get("/reddit-commentary/status/{task_id}")
async def get_task_status(task_id: str):
    return task_queue.get_task_status(task_id)
