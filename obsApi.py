import obswebsocket
from obswebsocket import obsws, requests
import time
import os
from dotenv import load_dotenv
from facebookApi import get_facebook_stream_key, brodcast_live_video  # Import the stream key function

# Load environment variables from .env file
load_dotenv()

OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))  # Convert to integer
# OBS_PASSWORD = os.getenv("OBS_PASSWORD")

<<<<<<< HEAD
def update_obs_stream_settings(stream_url):
=======
def update_obs_stream_settings(stream_key):
>>>>>>> d2a601b (Commit from facebook comp)
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
        client.connect()
        
        # Set new stream key in OBS
        client.call(requests.SetStreamSettings(
            type="rtmp_common",
            settings={
                "server": "rtmps://live-api-s.facebook.com:443/rtmp/",
            }
        ))

        print("✅ OBS Stream settings updated.")

        # Start streaming
        client.call(requests.StartStreaming())  # Start streaming
        time.sleep(5)  # Wait 5 seconds


        status = client.call(requests.GetStreamingStatus())  # Check if streaming started

        # Debugging - Print full response
        print("DEBUG: OBS Streaming Status Response:", status.datain)

        # Safely check if 'outputActive' exists
        is_streaming = status.datain.get("outputActive", "Field Missing")  

        # Safely check if 'outputActive' exists
        is_streaming = status.datain.get("outputActive", "Field Missing")

        # print("OBS Streaming Status:", status.getOutputActive())

        if is_streaming == "Field Missing":
            print("⚠️ WARNING: 'outputActive' not found in OBS response. Is OBS streaming?")
        else:
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
<<<<<<< HEAD
secure_stream_url = brodcast_live_video()

# Update OBS settings and start streaming
if secure_stream_url:
    update_obs_stream_settings(secure_stream_url)
=======
stream_key = get_facebook_stream_key()

# Update OBS settings and start streaming
if stream_key:
    update_obs_stream_settings( stream_key)
>>>>>>> d2a601b (Commit from facebook comp)
else:
    print("Failed to retrieve Facebook Live stream key.")