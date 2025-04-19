from typing import List, Dict
from ..clients.reddit_client import fetch_reddit_post_json

def extract_post_and_top_comments(url: str, top_n: int = 5) -> Dict:
    data = fetch_reddit_post_json(url)

    title = data[0]["data"]["children"][0]["data"]["title"]
    description = data[0]["data"]["children"][0]["data"]["selftext"]

    all_comments = data[1]["data"]["children"]
    comment_list = []

    for comment in all_comments:
        comment_data = comment.get("data", {})
        text = comment_data.get("body", "")
        upvotes_raw = comment_data.get("ups", 0)

        try:
            upvotes = int(upvotes_raw)
        except (ValueError, TypeError):
            upvotes = 0

        comment_list.append({"comment": text, "upvotes": upvotes})

    top_comments = sorted(comment_list, key=lambda x: x["upvotes"], reverse=True)[:top_n]

    return {
        "title": title,
        "description": description,
        "top_comments": top_comments
    }
