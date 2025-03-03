import obswebsocket
import obswebsocket.requests
import os
from dotenv import load_dotenv
from facebookApi import get_facebook_stream_key  # Import the stream key function

# Load environment variables from .env file
load_dotenv()

OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))  # Convert to integer
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def update_obs_stream_settings(stream_url, stream_key):
    client = obswebsocket.obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    
    try:
        client.connect()
        
        # Set new stream key in OBS
        client.call(obswebsocket.requests.SetStreamSettings(
            type="rtmp_common",
            settings={
                "server": stream_url,
                "key": stream_key
            }
        ))

        print("✅ OBS Stream settings updated.")

        # Start streaming
        client.call(obswebsocket.requests.StartStreaming())
        print("🎥 OBS Streaming started.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.disconnect()

# Get new stream key
stream_url, stream_key = get_facebook_stream_key()

# Update OBS settings and start streaming
if stream_url and stream_key:
    update_obs_stream_settings(stream_url, stream_key)
else:
    print("Failed to retrieve Facebook Live stream key.")
