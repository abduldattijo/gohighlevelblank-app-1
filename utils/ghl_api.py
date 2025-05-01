import requests
import json
from config import GHL_API_KEY, GHL_BASE_URL, LOCATION_ID

def get_headers():
    """Return headers for GoHighLevel API requests"""
    return {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Content-Type": "application/json"
    }

def get_social_accounts():
    """Get all connected social media accounts"""
    endpoint = f"{GHL_BASE_URL}social-media-posting/{LOCATION_ID}/accounts"
    
    try:
        response = requests.get(endpoint, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching social accounts: {e}")
        # Fallback to empty data if API fails
        return {"data": []}

def create_social_post(content, media_urls=None, scheduled_time=None, account_ids=None):
    """Create a social media post"""
    endpoint = f"{GHL_BASE_URL}social-media-posting/{LOCATION_ID}/posts"
    
    data = {
        "content": content,
        "mediaUrls": media_urls or [],
    }
    
    if account_ids:
        data["accounts"] = account_ids
    
    if scheduled_time:
        data["scheduledTime"] = scheduled_time
    
    try:
        response = requests.post(
            endpoint, 
            headers=get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating social post: {e}")
        return None

def get_posts(limit=10):
    """Get list of posts"""
    endpoint = f"{GHL_BASE_URL}social-media-posting/{LOCATION_ID}/posts/list"
    
    data = {
        "limit": limit,
        "offset": 0
    }
    
    try:
        response = requests.post(
            endpoint, 
            headers=get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")
        return {"data": []}