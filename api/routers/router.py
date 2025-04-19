from fastapi import APIRouter
from ..services.reddit_service import extract_post_and_top_comments
from ..clients.openai_client import generate_commentary_script

router = APIRouter()

@router.get("/reddit-commentary/")
def get_commentary_script(url: str):
    post_data = extract_post_and_top_comments(url)
    script = generate_commentary_script(post_data["title"], post_data["description"])
    return {"script": script}
