import os
import base64
import requests
from urllib.parse import urlparse
from typing import Dict

class RedditClient:
    """
    Fetches a Reddit post and its comments from a given URL.
    """
    def __init__(self):
        self.user_agent = 'ai-reels-builder/1.0 by TimTimer'
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.auth_headers = {
            'User-Agent': self.user_agent
        }

    def get_reddit_access_token(self):
        """Get Reddit API access token using client credentials."""
        client_id = os.getenv("REDDIT_APP_CLIENT_ID")
        client_secret = os.getenv("REDDIT_APP_SECRET_KEY")
        if not client_id or not client_secret:
            raise Exception("Reddit API credentials not found in environment variables")
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'User-Agent': self.user_agent
        }
        data = {'grant_type': 'client_credentials'}
        try:
            response = requests.post('https://www.reddit.com/api/v1/access_token', headers=headers, data=data, timeout=10)
            response.raise_for_status()
            token = response.json().get('access_token')
            if not token:
                raise Exception(f"No access_token in response: {response.text}")
            return token
        except requests.RequestException as e:
            raise Exception(f"Failed to get Reddit access token: {e}") from e

    def fetch_post_authenticated(self, url: str) -> Dict:
        """Fetch post using Reddit API authentication."""
        try:
            if '/s/' in url:
                response = requests.get(url, headers=self.headers, allow_redirects=True, timeout=10)
                response.raise_for_status()
                url = response.url
            parsed = urlparse(url)
            if 'reddit.com' not in parsed.netloc:
                raise Exception(f"Invalid Reddit URL: {url}")
            auth_url = url.replace('www.reddit.com', 'oauth.reddit.com')
            if not auth_url.endswith('.json'):
                auth_url += '.json'
            token = self.get_reddit_access_token()
            auth_headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.user_agent
            }
            response = requests.get(auth_url, headers=auth_headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Network error fetching Reddit post: {e}") from e
        except Exception as e:
            raise Exception(f"Error in fetch_post_authenticated: {e}") from e

    def extract_post_data(self, data: Dict, top_n: int = 5) -> Dict:
        """Extract title, description, and top comments from fetched post data."""
        try:
            title = data[0]["data"]["children"][0]["data"].get("title", "")
            description = data[0]["data"]["children"][0]["data"].get("selftext", "")
            all_comments = data[1]["data"].get("children", [])
            comment_list = []
            for comment in all_comments:
                comment_data = comment.get("data", {})
                text = comment_data.get("body", "")
                upvotes_raw = comment_data.get("ups", 0)
                try:
                    upvotes = int(upvotes_raw)
                except (ValueError, TypeError):
                    upvotes = 0
                if text:
                    comment_list.append({"comment": text, "upvotes": upvotes})
            top_comments = sorted(comment_list, key=lambda x: x["upvotes"], reverse=True)[:top_n]
            return {
                "title": title,
                "description": description,
                "top_comments": top_comments
            }
        except Exception as e:
            raise Exception(f"Failed to extract post data: {e}") from e

    def get_post_and_comments(self, url: str, top_n: int = 5) -> Dict:
        """Fetch a post and comments from a given URL and return the post data."""
        try:
            data = self.fetch_post_authenticated(url)
            post_data = self.extract_post_data(data, top_n)
            return post_data
        except Exception as e:
            raise Exception(f"Failed to fetch post and comments: {e}") from e