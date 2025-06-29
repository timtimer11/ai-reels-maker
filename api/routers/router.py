from fastapi import APIRouter
from clients.openai import generate_commentary_script, text_to_speech_file
from storage.cloudflare_s3 import CloudflareS3
from media.video import process_video_streaming
from utils.task_queue import task_queue, TaskStatus
from clients.reddit import RedditClient
import os
import asyncio
import traceback

router = APIRouter()

BUCKET_NAME = os.environ.get('CLOUDFLARE_TTS_BUCKET_NAME')

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
        print(f"Starting Reddit commentary processing for task {task_id} with URL: {url}")
        
        # Step 1: Get Reddit content
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_REDDIT_POST)
        print("Step 1: Fetching Reddit post and extracting data...")
        reddit_client = RedditClient()
        
        try:
            # Single function call that handles fetching and extracting
            # post_data = await asyncio.to_thread(reddit_client.get_post_and_comments, url, top_n=5)
            # print("Successfully fetched Reddit post and extracted data")
            post_data = reddit_client.get_post_and_comments(url, top_n=5)
            print("Successfully fetched Reddit post and extracted data")
        except Exception as e:
            error_msg = f"Error fetching and processing Reddit post: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e 
        
        # Step 2: Generate script
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_SCRIPT)
        print("Step 2: Generating script...")
        try:
            # script = await asyncio.to_thread(generate_commentary_script, post_data["title"], post_data["description"])
            script = generate_commentary_script(post_data["title"], post_data["description"])
            print("Successfully generated script")
        except Exception as e:
            error_msg = f"Error generating script: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        # Step 3: Generate audio
        task_queue.update_task_status(task_id, TaskStatus.GENERATING_VOICEOVER)
        print("Step 3: Generating voiceover...")
        try:
            # audio_speech = await asyncio.to_thread(text_to_speech_file, script)
            audio_speech = text_to_speech_file(script)
            cloudflare_s3.upload_file_to_s3(audio_speech, BUCKET_NAME, f"output_audio_{task_id}.mp3")
            print("Successfully generated voiceover and uploaded to S3")
        except Exception as e:
            error_msg = f"Error generating voiceover: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        # Step 4: Get video template
        task_queue.update_task_status(task_id, TaskStatus.FETCHING_BACKGROUND_VIDEO)
        print("Step 4: Fetching background video...")
        try:
            # subway_surfers_video = await asyncio.to_thread(cloudflare_s3.read_file_from_s3, BUCKET_NAME, "ss_background.mp4")
            subway_surfers_video = cloudflare_s3.read_file_from_s3(BUCKET_NAME, "ss_background.mp4")
            print("Successfully fetched background video")
        except Exception as e:
            error_msg = f"Error fetching background video: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        # Step 5: Process video
        task_queue.update_task_status(task_id, TaskStatus.PROCESSING_VIDEO)
        print("Step 5: Processing video...")
        try:
            # video_bytes = await asyncio.to_thread(process_video_streaming, audio_speech, subway_surfers_video)
            video_bytes = process_video_streaming(audio_speech, subway_surfers_video)
            print("Successfully processed video")
        except Exception as e:
            error_msg = f"Error processing video: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e

        # Step 6: Upload video to S3
        task_queue.update_task_status(task_id, TaskStatus.GETTING_VIDEO_URL)
        print("Step 6: Uploading video to S3...")
        try:
            # await asyncio.to_thread(cloudflare_s3.upload_file_to_s3, video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")
            cloudflare_s3.upload_file_to_s3(video_bytes, BUCKET_NAME, f"output_video_{task_id}.mp4")
            print("Successfully uploaded video to S3")
        except Exception as e:
            error_msg = f"Error uploading video to S3: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e

        # Step 7: Get S3 URL for the video
        print("Step 7: Getting video URL...")
        try:
            # video_url = await asyncio.to_thread(cloudflare_s3.get_s3_url, BUCKET_NAME, f"output_video_{task_id}.mp4")
            video_url = cloudflare_s3.get_s3_url(BUCKET_NAME, f"output_video_{task_id}.mp4")
            print(f"Successfully got video URL: {video_url}")
        except Exception as e:
            error_msg = f"Error getting video URL: {str(e)}"
            print(error_msg)
            task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
            raise e
        
        # Update task status to COMPLETED with video URL
        task_queue.update_task_status(task_id, TaskStatus.COMPLETED, video_url)
        print(f"Task {task_id} completed successfully!")
        
    except Exception as e:
        # If an error occurs, mark the task as failed
        error_msg = f"General error in process_reddit_commentary for task {task_id}: {str(e)}"
        print(error_msg)
        print(f"Full traceback: {traceback.format_exc()}")
        task_queue.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
        raise e

@router.get("/reddit-commentary/status/{task_id}")
async def get_task_status(task_id: str):
    return task_queue.get_task_status(task_id)
