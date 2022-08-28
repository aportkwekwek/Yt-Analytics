from tkinter import Y
from yt_analytics import Yt_Analytics

API_KEY="AIzaSyC_rCD1tyRluFqsXD76bEwQNVln9CqHwjU"
usrname=input("Enter username: ")

getdata = Yt_Analytics(API_KEY, usrname)
try:

    channel_id = getdata.get_usr_id()
except:
    channel_id = ""

if(channel_id != ""):
    getdata.get_usr_video_ids(channel_id)
    getdata.to_json_file()
else:
    print("NOT AVAILABLE")
