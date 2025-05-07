import asyncio
import websockets
import json
import os
import time
import requests
from dotenv import load_dotenv
from facebook_connect import brodcast_live_video  # Import your Facebook Live function
from obs_connect import send_obs_command

###########################################################################
#                                                                         #
#                             End Stream                                  #
#                                                                         #
###########################################################################

async def end_obs_stream():
    """Stops the OBS stream."""
    print("🛑 Ending OBS Stream...")

    response = await send_obs_command("StopStream")
    await asyncio.sleep(5)  # Give OBS time to stop

    print("Response: ", response)   


def delete_facebook_video(video_id):
    """Deletes the Facebook live video using Graph API."""
    access_token = os.getenv("FB_ACCESS_TOKEN")
    if not access_token or not video_id:
        print("❌ Missing access token or video ID.")
        return

    url = f"https://graph.facebook.com/v18.0/{video_id}"
    response = requests.delete(url, params={"access_token": access_token})
    
    if response.status_code == 200:
        print("✅ Facebook Live video deleted successfully.")
    else:
        print("❌ Failed to delete video:", response.text)


# Load environment variables
load_dotenv()

# Run the main function
asyncio.run(end_obs_stream())

# Delete the Facebook video after ending OBS stream
video_id = os.getenv("VIDEO_ID")
delete_facebook_video(video_id)
