import schedule
import time
import subprocess

def run_script():
    print("Running Facebook Live Script...")
    subprocess.run(["py", "obs_connect.py"])

# Schedule the script to run daily at 7:05 AM
schedule.every().day.at("08:46").do(run_script)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
