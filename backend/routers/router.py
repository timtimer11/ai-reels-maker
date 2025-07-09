import os
from fastapi import APIRouter
import asyncio
from clients.openai import OpenAIService
from clients.deepgram import DeepgramService
from storage.cloudflare_s3 import CloudflareS3
from media.video import process_video_streaming
from utils.task_queue import task_queue, TaskStatus
from clients.reddit import RedditClient

BUCKET_NAME = os.environ.get('CLOUDFLARE_TTS_BUCKET_NAME')

router = APIRouter()
cloudflare_s3 = CloudflareS3()
deepgram_service = DeepgramService()
openai_service = OpenAIService()

@router.post("/reddit-commentary")
async def start_reddit_commentary(url: str):
    """Create a task and start processing in background"""
    try:
        print("Processing Reddit commentary for URL:", url)
        task_id = task_queue.create_media_processing_task()
        task_queue.update_task_status(task_id, TaskStatus.PROCESSING)
        # Start processing in background
        asyncio.create_task(process_reddit_commentary(task_id, url))
        return {"task_id": task_id}
    except Exception as e:
        task_queue.update_task_status(task_id, TaskStatus.FAILED, error=str(e))
        raise

async def process_reddit_commentary(task_id: str, url: str):
    """Process Reddit commentary in background"""
    try:
        print("Fetching Reddit post and comments for URL:", url)
        # Get Reddit content
        reddit_client = RedditClient()
        try:
            post_data = reddit_client.get_post_and_comments(url, top_n=5)
        except Exception as e:
            error_msg = f"Error fetching and processing Reddit post: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e 
        
        print("Generating script for Reddit post")
        # Generate script
        try:
            script = openai_service.generate_commentary_script(post_data["title"], post_data["description"])
        except Exception as e:
            error_msg = f"Error generating script: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        print("Generating audio for Reddit post")
        # Generate audio
        try:
            audio_speech = deepgram_service.generate_audio_with_deepgram(script)
        except Exception as e:
            error_msg = f"Error generating voiceover: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        print("Fetching video template for Reddit post")
        # Get video template
        try:
            subway_surfers_video = cloudflare_s3.read_file_from_s3(BUCKET_NAME, "ss_background.mp4")
        except Exception as e:
            error_msg = f"Error fetching background video: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        print("Processing video for Reddit post")
        # Process video
        try:
            video_bytes = process_video_streaming(audio_speech, subway_surfers_video)
        except Exception as e:
            error_msg = f"Error processing video: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e

        print("Uploading video to S3 for Reddit post")
        # Upload video to S3
        try:
            cloudflare_s3.upload_file_to_s3(video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")
        except Exception as e:
            error_msg = f"Error uploading video to S3: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e

        print("Getting video URL for Reddit post")
        # Get S3 URL for the video
        try:
            video_url = cloudflare_s3.get_s3_url(BUCKET_NAME, f"output_video_{task_id}.mp4")
        except Exception as e:
            error_msg = f"Error getting video URL: {str(e)}"
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        print("Updating task status to COMPLETED with video URL")
        # Update task status to COMPLETED with video URL
        task_queue.update_task_status(task_id, TaskStatus.COMPLETED, video_url)
    except Exception as e:
        print("General error in process_reddit_commentary for task {task_id}: {str(e)}")
        # If an error occurs, mark the task as failed
        error_msg = f"General error in process_reddit_commentary for task {task_id}: {str(e)}"
        task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
        raise e

@router.get("/reddit-commentary/status/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a running task"""
    return task_queue.get_task_status(task_id)
