import re
from typing import Callable, Optional
from pytube import YouTube, Playlist
from pathlib import Path
import concurrent.futures


def is_playlist(url: str) -> bool:
    playlist_pattern = re.compile(
        r"https://www\.youtube\.com/playlist\?list=[0-9A-Za-z_-]+"
    )

    return bool(playlist_pattern.match(url))


def make_dir_for_playlist_download(playlist: Playlist, root_path: Path) -> Path:
    playlist_title = "".join(char if char.isalpha() else "" for char in playlist.title)
    playlist_folder_path = root_path.joinpath(playlist_title)

    if not playlist_folder_path.exists():
        playlist_folder_path.mkdir()
        print(f"New directory for playlist {playlist_title} created.")
    else:
        print(f"Directory {playlist_folder_path} for {playlist_title} exists.")

    return playlist_folder_path


def download_playlist(
    playlist: Playlist,
    playlist_path: Path,
    download_audio: Optional[Callable] = None,
    download_video: Optional[Callable] = None,
    workers: int = 6,
) -> None:
    urls = (lambda playlist: list(map(str, playlist)))(playlist)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

        if download_audio:
            futures = {
                executor.submit(download_audio, url, playlist_path): url for url in urls
            }
        if download_video:
            futures = {
                executor.submit(download_video, url, playlist_path): url for url in urls
            }

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")


def get_maxquality_audio_stream_itag(yt: YouTube) -> int:
    audio_streams = yt.streams.filter(only_audio=True)

    streams_quality_dict = {}
    for stream in audio_streams:
        streams_quality_dict[stream.itag] = stream.bitrate

    max_quality_itag = max(streams_quality_dict, key=streams_quality_dict.get)
    print(
        f"Selected itag: {max_quality_itag} quality -> {streams_quality_dict[max_quality_itag]}"
    )

    return max_quality_itag


def get_maxquality_video_stream_itag(yt: YouTube) -> int:
    video_streams = yt.streams.filter(only_video=True, file_extension="mp4")

    streams_quality_dict = {}
    for stream in video_streams:
        streams_quality_dict[stream.itag] = stream.resolution

    max_quality_itag = max(streams_quality_dict, key=streams_quality_dict.get)
    print(
        f"Selected itag: {max_quality_itag} resolution -> {streams_quality_dict[max_quality_itag]}"
    )

    return max_quality_itag
