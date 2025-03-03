import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def get_facebook_stream_key():
    url = f"https://graph.facebook.com/{PAGE_ID}/live_videos"
    params = {
        "access_token": ACCESS_TOKEN,
        "status": "LIVE_NOW",
        "fields": "id,stream_url,secure_stream_url"
    }
    response = requests.post(url, params=params)
    data = response.json()

    print("Full API Response:", json.dumps(data, indent=2))  # Debugging line

    if "error" in data:
        print("Error fetching stream key:", data["error"]["message"])
        return None, None

    stream_url = data.get("stream_url")
    stream_key = data.get("stream_key")

    return stream_url, stream_key

stream_url, stream_key = get_facebook_stream_key()
print(f"Stream URL: {stream_url}")
print(f"Stream Key: {stream_key}")
