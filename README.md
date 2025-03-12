# Automated-Facebook-live
This project uses Websockets to automatically stream from OBS to facebook daily at the time you set it up to.

# Install dependencies
```
py -m pip install websockets requests python-dotenv
```

# How to configure 
Add a .env file to your project directory and add ACCESS_TOKEN and PAGE_ID so that you are able to extract the facebooks stream key with proper authentication. Also add OBS_HOST=localhost, OBS_PORT=4455 and if you configure OBS websocket to have authentication also add OBS_PASSWORD=yourpassword. The last thing you need is FACEBOOK_STREAM_TITLE=TITLE, and FACEBOOK_STREAM_DESCRIPTION=DESCRIPTION. Keep in mind that this last two are required for the stream. 

To run the program, you need to get in the project directory and depending on what version of python you have run 'py gui.py' which will run the graphical interface and also initiate the database. On the GUI, add at what time 