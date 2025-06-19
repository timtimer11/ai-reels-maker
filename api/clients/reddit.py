import requests
from typing import Dict

class RedditClient:
    """
    This class is used to fetch a post and its comments from a given URL and return the post data.
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

    def fetch_post(self, url: str) -> Dict:
        """
        Fetches a post and its comments from a given URL and returns the post data.
        """
        url_processed = url + ".json"
        response = requests.get(url_processed, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch Reddit post. Status code: {response.status_code}")

    def extract_post_data(self, data: Dict, top_n: int = 5) -> Dict:
        """
        Extracts the post data from the fetched post.
        """
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

    def get_post_and_comments(self, url: str, top_n: int = 5) -> Dict:
        """
        Fetches a post and its comments from a given URL and returns the post data.
        """
        data = self.fetch_post(url)
        return self.extract_post_data(data, top_n)
