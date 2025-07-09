import requests
import base64
import os
from typing import Dict
from urllib.parse import urlparse

class RedditClient:
    """
    This class is used to fetch a post and its comments from a given URL and return the post data.
    """
    def __init__(self):
        """
        Initialize RedditClient with default headers.
        """
        self.user_agent = 'ai-reels-builder/1.0 by TimTimer'
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    
    def get_reddit_access_token(self):
        """Get Reddit API access token using client credentials"""
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
        """Fetch post using Reddit API authentication"""
        try:
            # Handle mobile short URLs
            if '/s/' in url:
                resp = requests.get(url, headers=self.headers, allow_redirects=True, timeout=10)
                resp.raise_for_status()
                url = resp.url
            # Normalize Reddit URLs
            parsed = urlparse(url)
            netloc = parsed.netloc
            if 'reddit.com' not in netloc:
                raise Exception(f"Invalid Reddit URL: {url}")
            # Replace to oauth endpoint
            auth_url = url.replace('www.reddit.com', 'oauth.reddit.com').replace('reddit.com', 'oauth.reddit.com')
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
            raise Exception(f"Network error fetching Reddit pos    t: {e}") from e
        except Exception as e:
            raise Exception(f"Error in fetch_post_authenticated: {e}") from e

    def extract_post_data(self, data: Dict, top_n: int = 5) -> Dict:
        """Extract the post data from the fetched post"""
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
                if text:  # Only include non-empty comments
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
        """Fetch a post and comments from a given URL and returns the post data"""
        try:
            data = self.fetch_post_authenticated(url)
            post_data = self.extract_post_data(data, top_n)
            return post_data
        except Exception as e:
            raise Exception(f"Failed to fetch post and comments: {e}") from e
