import obswebsocket
from obswebsocket import obsws, requests
import time
import os
from dotenv import load_dotenv
from facebookApi import get_facebook_stream_key, brodcast_live_video  # Import the stream key function
import json 

# Load environment variables from .env file
load_dotenv()

OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))  # Convert to integer
# OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def update_obs_stream_settings(stream_url):

    client = obsws(OBS_HOST, OBS_PORT)

    # try:
    #     print("🔗 Connecting to OBS WebSocket...")
    #     client.connect()
    #     print("✅ Successfully connected to OBS WebSocket!")

    #     status = client.call(requests.GetStreamingStatus())
    #     print("🔍 OBS Streaming Status Response:", status.datain)

    # except Exception as e:
    #     print(f"❌ OBS WebSocket Connection Error: {e}")
    # finally:
    #     client.disconnect()
    
    try:

        print("🔗 Connecting to OBS WebSocket...")

        client.connect()
        
        print("🚀 Setting OBS Stream Key...")
        # Set new stream key in OBS
        client.call(requests.SetStreamSettings(
            type="rtmp_common",
            settings={
                "server": "rtmps://live-api-s.facebook.com:443/rtmp/",
                "key": stream_url.split("/")[-1],  # Extract the stream key (the part after '/rtmp/')   
            }
        ))

        print("✅ OBS Stream Key Set.")

        time.sleep(3)

        print("✅ Starting OBS Stream...")

        # Start streaming
        client.call(requests.StartStreaming())  # Start streaming
        time.sleep(15)  # Wait 5 seconds


        print("🔍 Checking OBS Streaming Status...")

        # Subscribe to streaming status updates
        client.call(requests.SetCurrentScene(scene_name="Scene"))  # Set scene to force update
        client.call(requests.SetHeartbeat(True))  # Request regular status updates

        time.sleep(2)  # Allow time for OBS to update status

        # status = client.call(requests.GetStreamingStatus()) 
        # print("DEBUG: OBS Streaming Status Response:", status.datain)

        # Check if OBS is streaming
        try:
            status = client.call(requests.GetStreamingStatus())
            print("DEBUG: OBS Streaming Status Response:", status.datain)
            is_streaming = status.getOutputActive() if hasattr(status, "getOutputActive") else "Field Missing"
        except Exception as e:
            print(f"❌ OBS Error: {e}")
            is_streaming = "Failed"

        print("✅ OBS Streaming Status:", is_streaming)


    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.disconnect()

# # Get new stream key
# stream_key = get_facebook_stream_key()

# # Update OBS settings and start streaming
# if  stream_key:
#     update_obs_stream_settings(stream_key)
# else:
#     print("Failed to retrieve Facebook Live stream key.")


# Get new stream key
secure_stream_url = brodcast_live_video()

# Update OBS settings and start streaming
if secure_stream_url:
    update_obs_stream_settings(secure_stream_url)
else:
    print("Failed to retrieve Facebook Live stream key.")