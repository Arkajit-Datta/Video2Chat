from yt_dlp import YoutubeDL
import os

# Replace the playlist URL with your desired playlist URL
playlist_url = 'https://youtube.com/playlist?list=PL_PgxS3FkP7ATPveBQ1yah7LDqysyzDCG&si=GUM8RS-uuvVfV8GH'

ydl_opts = {
    'format': 'best',
    'ignoreerrors': True,
    'quiet': False,
    'no_warnings': False,
    'playlistend': None,
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}

# Create the downloads directory if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])