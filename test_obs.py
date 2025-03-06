from obswebsocket import obsws, requests
import time

OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_obs_password"  # Set this if you have authentication

client = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)

try:
    print("🔗 Connecting to OBS WebSocket...")
    client.connect()
    print("✅ Connected!")

    print("🔍 Checking OBS Streaming Status (Before StartStreaming)...")
    status = client.call(requests.GetStreamingStatus())
    print("DEBUG: Streaming Status Before:", status.datain)

    print("🚀 Starting OBS Stream...")
    client.call(requests.StartStreaming())

    time.sleep(8)  # Give OBS time to start

    print("🔍 Checking OBS Streaming Status (After StartStreaming)...")
    status = client.call(requests.GetStreamingStatus())
    print("DEBUG: Streaming Status After:", status.datain)

except Exception as e:
    print(f"❌ OBS Error: {e}")
finally:
    client.disconnect()
