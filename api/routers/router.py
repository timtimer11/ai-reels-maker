from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services.reddit_service import extract_post_and_top_comments
from ..clients.openai_client import generate_commentary_script, text_to_speech_file
from ..clients.s3_client import read_file_from_s3
from ..clients.video_client import process_video_streaming
import os
from dotenv import load_dotenv
router = APIRouter()

load_dotenv()

BUCKET_NAME = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')

@router.get("/reddit-commentary", response_model=Dict[str, str])
async def get_commentary_script(url: str):
    try:
        post_data = extract_post_and_top_comments(url)
        # post_data = 'Testing'
        print('1. Extract Reddit Post SUCCESS')
        script = generate_commentary_script(post_data["title"], post_data["description"])
        # script = 'Testing'
        print('2. Generate Commentary Script SUCCESS')

        audio_speech = text_to_speech_file(text=script)
        print('3. Generate Audio SUCCESS')
        subway_surfers_video = read_file_from_s3(bucket_name=BUCKET_NAME, file_name="subway_surfers.mp4")
        print('4. Read Video SUCCESS')
        combined_video_audio = process_video_streaming(audio_speech, subway_surfers_video)
        print('5. Process Video SUCCESS')
        with open("processed_video.mp4", "wb") as f:
            f.write(combined_video_audio)
        print('6. Write Video SUCCESS')
        return { 'status': 'true' }
    except Exception as e:
        print(f"Error in get_commentary_script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
