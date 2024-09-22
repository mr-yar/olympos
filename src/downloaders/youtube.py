# Create a YoutubeDL instance

from yt_dlp import YoutubeDL

default_options = {'quiet': True, 'format': 'bv+ba/b', 'noplaylist': True, 'merge_output_format': 'mp4'}


def download_youtube_video_best_quality(url: str, user_id: str, options=default_options) -> None:
    ydl_opts = {**options, 'outtmpl': f'./downloads/{user_id}//%(title)s.%(ext)s'}

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info_dict)

        # Output the filename
        print(f"The filename would be: {filename}")

        return filename
