import requests
import base64
import os
from typing import Dict

class RedditClient:
    """
    This class is used to fetch a post and its comments from a given URL and return the post data
    """
    def __init__(self):
        self.auth_headers = {
            'User-Agent': 'ai-reels-builder/1.0 by TimTimer'
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
            'User-Agent': self.auth_headers['User-Agent']
        }
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post('https://www.reddit.com/api/v1/access_token', 
                               headers=headers, data=data)
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to get Reddit access token: {response.text}")
    
    def fetch_post_authenticated(self, url: str) -> Dict:
        """Fetch post using Reddit API authentication"""
        try:
            if '/s/' in url:
                response = requests.get(url, headers=self.auth_headers, allow_redirects=True, timeout=10)
                url = response.url
            
            # Get access token
            token = self.get_reddit_access_token()
            
            # Convert URL to OAuth endpoint
            if 'reddit.com' in url:
                auth_url = url.replace('www.reddit.com', 'oauth.reddit.com')
                if not auth_url.endswith('.json'):
                    auth_url += '.json'
            else:
                raise ValueError("Invalid Reddit URL")
            
            # Make authenticated request
            auth_headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': self.auth_headers['User-Agent']
            }
            
            response = requests.get(auth_url, headers=auth_headers, timeout=10)
            print('Authenticated response received')
            
        except requests.RequestException as e:
            print(f'{e}')
            raise Exception(f"Network error fetching Reddit post: {e}")
        
        if response.status_code == 200:
            print('Authenticated response received with Status=200')
            return response.json()
        else:
            print(f'Auth request failed with status: {response.status_code}')
            raise Exception(f"Failed to fetch Reddit post with auth. Status code: {response.status_code}")

    def extract_post_data(self, data: Dict, top_n: int = 5) -> Dict:
        """
        Extract the post data from the fetched post
        """
        try:
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
        except Exception as e:
            print(e)

    def get_post_and_comments(self, url: str, top_n: int = 5) -> Dict:
        """
        Fetch a post and its comments from a given URL and return the post data
        """
        try:
            data = self.fetch_post_authenticated(url)
            post_data = self.extract_post_data(data, top_n)
            return post_data
        except Exception as e:
            print(f"Authenticated request failed: {e}")