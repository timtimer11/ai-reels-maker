import requests

def fetch_reddit_post_json(url: str) -> dict:
    headers = {'User-Agent': 'Mozilla/5.0'}
    url_processed = url + ".json"
    response = requests.get(url_processed, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch Reddit post. Status code: {response.status_code}")
