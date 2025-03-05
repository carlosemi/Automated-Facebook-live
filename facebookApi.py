import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
FACEBOOK_STREAM_TITLE = os.getenv("FACEBOOK_STREAM_TITLE")
FACEBOOK_STREAM_DESCRIPTION = os.getenv("FACEBOOK_STREAM_DESCRIPTION")

###########################################################################
#                                                                         #
#                        Get Facebook Stream Key                          #
#                                                                         #
###########################################################################

def get_facebook_stream_key():
    url = f"https://graph.facebook.com/{PAGE_ID}/live_videos"
    params = {
        "access_token": ACCESS_TOKEN,
        "status": "LIVE_NOW",
        "fields": "id,stream_url, secure_stream_url"
    }
    response = requests.post(url, params=params)
    data = response.json()

    print("Full API Response:", json.dumps(data, indent=2))  # Debugging line

    if "error" in data:
        print("Error fetching stream key:", data["error"]["message"])
        return None, None

    # stream_url = data.get("stream_url")
    # stream_key = data.get("stream_key")

    secure_stream_url = data.get("secure_stream_url")

    if not secure_stream_url:
        print("Error: Stream URL not found in response.")
        return None, None
    
    return stream_key

    '''
    stream_url = data.get("stream_url")

        if not stream_url:
            print("⚠️ No secure stream URL found in API response.")
            return None

    # Extract the stream key (the part after '/rtmp/')
    stream_key = stream_url.split("/")[-1]

    return stream_key

    # stream_url = data.get("stream_url")
    # stream_key = data.get("stream_key")

    # return stream_url, stream_key
    '''


###########################################################################
#                                                                         #
#                 Start Live Video Broadcast on Facebook                  # 
#                                                                         #
###########################################################################

def brodcast_live_video():
    url = f"https://graph.facebook.com/v22.0/{PAGE_ID}/live_videos"
    params = {
        "access_token": ACCESS_TOKEN,
        "status": "LIVE_NOW",
        "title": FACEBOOK_STREAM_TITLE,
        "description": FACEBOOK_STREAM_DESCRIPTION,
    }
    response = requests.post(url, params=params)
    data = response.json()

    # print("Full API Response:", json.dumps(data, indent=2))  # Debugging line

    if "error" in data:
        print("Error starting live video broadcast:", data["error"]["message"])
        return

    print("🎥 Live video broadcast started successfully.")

    secure_stream_url = data.get("secure_stream_url")

    print(f"Stream URL: {secure_stream_url}")

    return secure_stream_url


###########################################################################
#                                                                         #
#                                 TEST                                    # 
#                                                                         #
###########################################################################


# stream_url, stream_key = get_facebook_stream_key()
# print(f"Stream URL: {stream_url}")
# print(f"Stream Key: {stream_key}")

brodcast_live_video()
