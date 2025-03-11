import asyncio
import websockets
import json
import os
import time
from dotenv import load_dotenv
from facebookApi import brodcast_live_video  # Import your Facebook Live function

# Load environment variables
load_dotenv()

OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = os.getenv("OBS_PORT")
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

# Generate request ID counter
request_id = 1

###########################################################################
#                                                                         #
#                        Send Commands To OBS                             #
#                                                                         #
###########################################################################

async def send_obs_command(command, params={}):
    """Sends a command to OBS WebSocket and returns the response."""
    global request_id
    request_id += 1

    async with websockets.connect(f"ws://{OBS_HOST}:{OBS_PORT}") as websocket:
        print(f"🔗 Connected to OBS WebSocket on {OBS_HOST}:{OBS_PORT}")

        # Step 1: Send Identify message before any other command
        identify_request = {
            "op": 1,  # Identify operation
            "d": {
                "rpcVersion": 1  # Required for WebSocket 5+
            }
        }
        await websocket.send(json.dumps(identify_request))
        identify_response = await websocket.recv()
        identify_json = json.loads(identify_response)
        print(f"✅ OBS WebSocket Identified: {json.dumps(identify_json, indent=2)}")

        # Step 2: Now send the actual command
        request = {
            "op": 6,  # Request operation
            "d": {
                "requestType": command,
                "requestId": str(request_id),
                "requestData": params if params else {}
            }
        }

        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        response_json = json.loads(response)

        print(f"🔍 OBS Response ({command}): {json.dumps(response_json, indent=2)}")
        return response_json



###########################################################################
#                                                                         #
#                        Get Facebook Stream Key                          #
#                                                                         #
###########################################################################

async def authenticate(websocket):
    """Authenticates with OBS WebSocket if a password is required."""
    auth_request = {
        "op": 1  # Identify request
    }
    await websocket.send(json.dumps(auth_request))
    auth_response = await websocket.recv()
    auth_data = json.loads(auth_response)
    
    if auth_data["op"] == 2 and "authentication" in auth_data["d"]:
        auth_string = auth_data["d"]["authentication"]
        auth_payload = {
            "op": 3,
            "d": {
                "authentication": auth_string
            }
        }
        await websocket.send(json.dumps(auth_payload))
        auth_confirm = await websocket.recv()
        print("✅ Authenticated with OBS")



###########################################################################
#                                                                         #
#                  Set OBS Stream Settings & Stream                       #
#                                                                         #
###########################################################################

async def update_obs_stream_settings(stream_url):
    """Updates the OBS stream key and starts the stream."""

    stream_key = stream_url.split("/")[-1]  # Extract the stream key

    print("🚀 Setting OBS Stream Key...")

    await send_obs_command("SetStreamServiceSettings", {
        "streamServiceType": "rtmp_common",
        "streamServiceSettings": {
            "server": "rtmps://live-api-s.facebook.com:443/rtmp/",
            "key": stream_key
        }
    })
    time.sleep(3)  # Allow time for OBS to apply settings

    print("✅ Starting OBS Stream...")
    response = await send_obs_command("StartStream")
    await asyncio.sleep(5)  # Give OBS time to start

    # if response.get("d", {}).get("requestStatus", {}).get("code") == 100:
    #     print("✅ OBS Stream Started Successfully!")
    # else:
    #     print("❌ OBS StartStream Command Failed!")

    time.sleep(5)  # Give OBS time to start streaming

    print("🔍 Checking OBS Streaming Status...")
    status = await send_obs_command("GetStreamStatus")

    # Extracting outputActive correctly for OBS 5+
    is_streaming = status.get("d", {}).get("outputActive", False)

    # if is_streaming:
    #     print("✅ OBS is Streaming!")
    # else:
    #     print("❌ OBS is NOT Streaming!")


###########################################################################
#                                                                         #
#                                 Main                                    #
#                                                                         #
###########################################################################
async def main():
    """Main function to get stream key and start OBS streaming."""
    secure_stream_url = brodcast_live_video()  # Get Facebook Live stream key

    if secure_stream_url:
        await update_obs_stream_settings(secure_stream_url)
    else:
        print("❌ Failed to retrieve Facebook Live stream key.")

# Run the main function
asyncio.run(main())
