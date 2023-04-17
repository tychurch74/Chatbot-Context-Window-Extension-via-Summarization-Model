# yt_data.py
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import urllib.parse as p
import re
import os
import pickle
import json

# Gets data from Youtube channels specified in a .json file
class YoutubeData:
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    def __init__(self):
        self.youtube = self.authenticate()

    def authenticate(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "credentials.json"
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build(api_service_name, api_version, credentials=creds)

    def get_video_id_by_url(self, url):
        parsed_url = p.urlparse(url)
        video_id = p.parse_qs(parsed_url.query).get("v")
        if video_id:
            return video_id[0]
        else:
            raise Exception(f"Wasn't able to parse video URL: {url}")

    def get_video_details(self, **kwargs):
        return self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            **kwargs
        ).execute()
    
    def print_video_infos(self, video_response):
        items = video_response.get("items")[0]
        # get the snippet, statistics & content details from the video response
        snippet         = items["snippet"]
        statistics      = items["statistics"]
        content_details = items["contentDetails"]
        # get infos from the snippet
        channel_title = snippet["channelTitle"]
        title         = snippet["title"]
        description   = snippet["description"]
        publish_time  = snippet["publishedAt"]
        # get stats infos
        comment_count = statistics["commentCount"]
        like_count    = statistics["likeCount"]
        view_count    = statistics["viewCount"]
        # get duration from content details
        duration = content_details["duration"]
        # duration in the form of something like 'PT5H50M15S'
        # parsing it to be something like '5:50:15'
        parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
        duration_str = ""
        for d in parsed_duration:
            if d:
                duration_str += f"{d[:-1]}:"
        duration_str = duration_str.strip(":")
        print(f"""\
        Title: {title}
        Description: {description}
        Channel Title: {channel_title}
        Publish time: {publish_time}
        Duration: {duration_str}
        Number of comments: {comment_count}
        Number of likes: {like_count}
        Number of views: {view_count}
        """)


    def get_video_infos(self, video_response):
        items = video_response.get("items")[0]
        snippet = items["snippet"]
        statistics = items["statistics"]
        content_details = items["contentDetails"]
        channel_title = snippet["channelTitle"]
        title = snippet["title"]
        description = snippet["description"]
        duration = content_details["duration"]
        parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
        duration_str = ""

        for d in parsed_duration:
            if d:
                duration_str += f"{d[:-1]}:"
        duration_str = duration_str.strip(":")

        video_stats = {
            'channel_title': channel_title,
            'title': title,
            'duration': duration_str,
            'description': description
        }
        return video_stats

    def search(self, **kwargs):
        return self.youtube.search().list(
            part="snippet",
            **kwargs
        ).execute()

    def parse_channel_url(self, url):
        path = p.urlparse(url).path
        id = path.split("/")[-1]
        if "/c/" in path:
            return "c", id
        elif "/channel/" in path:
            return "channel", id
        elif "/user/" in path:
            return "user", id

    def get_channel_id_by_url(self, url):
        method, id = self.parse_channel_url(url)
        if method == "channel":
            return id
        elif method == "user":
            response = self.get_channel_details(forUsername=id)
            items = response.get("items")
            if items:
                channel_id = items[0].get("id")
                return channel_id
        elif method == "c":
            response = self.search(q=id, maxResults=1)
            items = response.get("items")
            if items:
                channel_id = items[0]["snippet"]["channelId"]
                return channel_id
        raise Exception(f"Cannot find ID:{id} with {method} method")

    def get_channel_videos(self, **kwargs):
        return self.youtube.search().list(
            **kwargs
        ).execute()

    def get_channel_details(self, **kwargs):
        return self.youtube.channels().list(
            part="statistics,snippet,contentDetails",
            **kwargs
        ).execute()

    def create_data_object(self, video_url, video_stats):
        data_object = {
            'url': video_url,
            'channel_title': video_stats['channel_title'],
            'title': video_stats['title'],
            'duration': video_stats['duration'],
            'description': video_stats['description']
        }
        return data_object

    def add_url_to_json_file(self, json_file, video_url):
        try:
            with open(json_file, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.append(video_url)

        with open(json_file, 'w') as f:
            json.dump(existing_data, f, indent=4)


channel_url_list = 'yt_channel_urls.json'

with open(channel_url_list, 'r') as file:
    data = json.load(file)

for index, entry in enumerate(data):
    youtube_data = YoutubeData()
    youtube = youtube_data.authenticate()
    channel_url = entry['link']
    channel_id = youtube_data.get_channel_id_by_url(channel_url)
    response = youtube_data.get_channel_details(id=channel_id)
    # extract channel infos
    snippet = response["items"][0]["snippet"]
    statistics = response["items"][0]["statistics"]
    #channel_country = snippet["country"]
    channel_description = snippet["description"]
    channel_creation_date = snippet["publishedAt"]
    channel_title = snippet["title"]
    channel_subscriber_count = statistics["subscriberCount"]
    channel_video_count = statistics["videoCount"]
    channel_view_count  = statistics["viewCount"]
    print(f"""
    Title: {channel_title}
    Published At: {channel_creation_date}
    Description: {channel_description}
    
    Number of videos: {channel_video_count}
    Number of subscribers: {channel_subscriber_count}
    Total views: {channel_view_count}
    """)

    # the following is grabbing channel videos
    # number of pages you want to get
    n_pages = 5
    # counting number of videos grabbed
    n_videos = 0

    next_page_token = None
    for i in range(n_pages):
        params = {
            'part': 'snippet',
            'q': '',
            'channelId': channel_id,
            'type': 'video',
        }
        if next_page_token:
            params['pageToken'] = next_page_token
        res = youtube_data.get_channel_videos(**params)
        channel_videos = res.get("items")
        for video in channel_videos:
            n_videos += 1
            json_file = 'yt_video_data.json'
            video_id = video["id"]["videoId"]
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_response = youtube_data.get_video_details(id=video_id)
            print(f"================Video #{n_videos}================")
            try:
                youtube_data.print_video_infos(video_response)
                print(f"Video URL: {video_url}")
                video_stats = youtube_data.get_video_infos(video_response)
                data_object = youtube_data.create_data_object(video_url, video_stats)
                youtube_data.add_url_to_json_file(json_file, data_object)
                print("="*40)
            except:
                print("Video not found")
        print("*"*100)
        
        if "nextPageToken" in res:
            next_page_token = res["nextPageToken"]
     