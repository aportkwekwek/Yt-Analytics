from fileinput import filename
from ssl import CHANNEL_BINDING_TYPES
import requests
import json


class Yt_Analytics:
    def __init__(self, API_KEY, USRNAME):
        self.self = self
        self.API_KEY = API_KEY
        self.USRNAME = USRNAME
        self.channel_stats = None
        self.video_data = None

    def get_usr_id(self):
        url=f'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={self.USRNAME}&key={self.API_KEY}'

        json_url = requests.get(url)
        data = json.loads(json_url.text)

        try:
            channel_id = data["items"][0]["id"]
            data = data['items'][0]['statistics']

        except Exception as ex:
            print(ex)
            data = None
        
        self.channel_stats = data
        return channel_id

    def get_usr_video_ids(self , usrid):
        if(usrid == None):
            return
        list_usr_videos = self._get_usr_videos(usrid, limit=50)

        parts = ["snippet","statistics","contentDetails"]
        for video_id in list_usr_videos:
            for part in parts:
                data = self._get_video_statistics(part, video_id)
                list_usr_videos[video_id].update(data)
        
        self.video_data = list_usr_videos
        return list_usr_videos

    def _get_video_statistics(self, part,video_id):
        url=f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.API_KEY}'

        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            # print(data)
            data = data['items'][0][part]

        except Exception as ex:
            print(ex)
            data = dict()
        
        return data
        

    def _get_usr_videos(self, usrid,limit = None):

        url=f'https://www.googleapis.com/youtube/v3/search?key={self.API_KEY}&channelId={usrid}&part=id&order=date'
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
            
        videos, npt = self._get_usr_video_perpage(url)
        idx = 0
        while(npt is not None and idx < 10):
            nextUrl = url + "&pageToken=" + str(npt)
            next_vid, npt = self._get_usr_video_perpage(nextUrl)
            videos.update(next_vid)
            idx += 1
        
        return videos

    def _get_usr_video_perpage(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_ids = dict()
        if 'items' not in data:
            return channel_ids, None 

        item_data = data['items']
        nextpage_token = data.get("nextPageToken", None)
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == "youtube#video":
                    video_id = item['id']['videoId']
                    channel_ids[video_id] = dict()
            except Exception as ex:
                print(ex)

        return channel_ids , nextpage_token

    def to_json_file(self):
        if self.channel_stats is None or self.video_data is None:
            print("No data")
            return
        
        data_combined = {self.USRNAME: {"channel statistics" : self.channel_stats , "video data": self.video_data}}

        channel_title = self.USRNAME
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(data_combined, f , indent=4)
        
        print('dumped')