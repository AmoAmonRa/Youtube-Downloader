import yt_dlp
video = False
music_down_adderess = r''
def yt_down(url):
    if video:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',        # Select best video and best audio
            'merge_output_format': 'mp4',                # Output format after merging             # Path to ffmpeg executable
            'outtmpl': '%(title)s.%(ext)s',              # Output file naming template
            'quiet': False,                              # Show download progress
            'noplaylist': True                           # Download only one video if playlist
        }
    else:
        ydl_opts = {
            'outtmpl': rf'{music_down_adderess}\%(title)s.%(ext)s',
            'format': 'mp3/bestaudio/best',
            'keepvideo':False,
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and         their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    with yt_dlp.YoutubeDL(ydl_opts , )as song:
        for x in url:
            song.download(x)
url = input('YouTube URL (Separate with comma) : ')
all_url = url.split(',')
yt_down(all_url)
