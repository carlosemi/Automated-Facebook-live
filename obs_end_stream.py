import asyncio
import websockets
import json
import os
import time
from dotenv import load_dotenv
from facebookApi import brodcast_live_video  # Import your Facebook Live function
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
    # if response.get("d", {}).get("requestStatus", {}).get("code") == 100:
    #     print("✅ OBS Stream Ended Successfully!")
    # else:
    #     print("❌ OBS StopStream Command Failed!")


# Run the main function
asyncio.run(end_obs_stream())