# Automated Facebook Live

Automate your Facebook Live streams using OBS and Websockets. This project schedules daily streams at a specified time, automatically starting and stopping the broadcast.

---

## Installation

Ensure you have Python installed, then install the required dependencies:

```bash
py -m pip install websockets requests python-dotenv
```

---

## Configuration

1. Create a `.env` file in your project directory and add the following variables:

   ```ini
   ACCESS_TOKEN=your_facebook_access_token
   PAGE_ID=your_facebook_page_id
   OBS_HOST=localhost
   OBS_PORT=4455
   OBS_PASSWORD=your_obs_password  # Only required if OBS WebSocket authentication is enabled
   FACEBOOK_STREAM_TITLE=Your Stream Title
   FACEBOOK_STREAM_DESCRIPTION=Your Stream Description
   ```

2. These variables are essential for authenticating with Facebook, retrieving the stream key, and connecting to OBS.

---

## Usage

1. Navigate to the project directory.
2. Run the graphical interface using:

   ```bash
   py gui.py
   ```

   This will initialize the database and allow you to schedule stream times.

3. On the GUI, add the times at which you want the stream to start.
4. The program will automatically schedule the stream's end time.

---

## Customizing the Stream Duration

To modify the stream duration, adjust the `load_schedules_from_db` function in the code:

```python
def load_schedules_from_db():
    """
    Clears the current schedule and re-adds jobs based on database entries.
    """
    schedule.clear()
    rows = get_schedules()
    for row in rows:
        schedule_time = row[1]  # 'HH:MM' format

        # Schedule the stream start time
        schedule.every().day.at(schedule_time).do(run_script)

        # Define the stream end time
        hour, minute = map(int, schedule_time.split(":"))
        end_hour = (hour + 7) % 24  # Adjust as needed
        end_minute = (minute + 50) % 60  # Adjust as needed

        scheduled_end = f"{end_hour:02d}:{end_minute:02d}"
        print(f"Stream will end at: {scheduled_end}")

        # Automatically end the stream after the specified duration
        schedule.every().day.at(scheduled_end).do(end_obs_stream)
```

### Adjusting the Stream End Time:
- Modify `end_hour = (hour + 7) % 24` to set the number of hours after the stream starts before ending.
- Modify `end_minute = (minute + 50) % 60` to adjust the minutes.

---

## Features
✅ **Automates Facebook Live streams**  
✅ **Uses OBS WebSockets for control**  
✅ **Schedules daily streams**  
✅ **Allows custom stream durations**  
✅ **Graphical interface for ease of use**  

---

## License

This project is licensed under the MIT License. Feel free to use and modify it.

---

## Contributions

Contributions, bug reports, and feature suggestions are welcome! Feel free to submit an issue or pull request.
