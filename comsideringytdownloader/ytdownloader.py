import os
import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Ask the user for their YouTube API key
api_key = input("Enter your YouTube API key: ")

# Use the YouTube Data API to search for videos on YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

# Ask the user for the search query
query = input("Enter your search query: ")

# Use the search.list method to search for videos matching the query
request = youtube.search().list(
    part='id,snippet',
    type='video',
    q=query
)

# Execute the request and store the response
response = request.execute()

# Print the titles of the videos in the response
for item in response['items']:
    print(item['snippet']['title'])


# Get the ID of the first video from the search results
video_id = response['items'][0]['id']['videoId']

# Use the videos.list method to retrieve the details of the video
request = youtube.videos().list(
    part='id,snippet',
    id=video_id
)

# Execute the request and store the response
response = request.execute()

# Extract the URL of the video from the response
video_url = str(f"https://www.youtube.com/watch?v={video_id}")

#options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Use the youtube-dl library to download the video
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([{video_url}])
