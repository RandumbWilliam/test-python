import subprocess
from pytube import Playlist

playlistLink = "https://www.youtube.com/playlist?list=PLoQsMDseU_UEVJ3N8btjy0XyeyodWwT1e"
playlist = Playlist(playlistLink)

downloadDirectory = "./ece406-lecs"

for video in playlist.videos:
    video.streams.filter(type="video", progressive=True, file_extension="mp4").order_by('resolution').desc().first().download(downloadDirectory)