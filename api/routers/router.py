from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict

router = APIRouter()

@router.get("/reddit-commentary/", response_model=Dict[str, str])
async def get_commentary_script(url: str):
    try:
        # post_data = extract_post_and_top_comments(url)
        post_data = 'Testing'
        print('post data: ', post_data)
        # script = generate_commentary_script(post_data["title"], post_data["description"])
        script = 'Testing'
        print('Returning script:', script)
        
        return {"script": script}
    except Exception as e:
        print(f"Error in get_commentary_script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
