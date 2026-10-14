import os
import csv
import logging
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from yt_dlp import YoutubeDL
from yt_dlp.networking.impersonate import ImpersonateTarget
from yt_dlp.utils import sanitize_filename


working_dir = 'video_scrapper'
logs_path = os.path.join(working_dir, 'download.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_path),    # Log to file
        logging.StreamHandler()    # Log to console
    ]
)


def set_download_folder() -> Path:
    """Return the download folder path from ENV or config file."""
    load_dotenv()
    env_path = os.getenv('DOWNLOAD_FOLDER')
    if env_path:
        return Path(env_path)

    raise RuntimeError(
        'No DOWNLOAD_FOLDER environment variable set. '
        'Set DOWNLOAD_FOLDER.'
    )


def download_video(url, name, aria2c_args):
    """Download function to download video from URL"""
    ydl_opts = {
            # XXX on demand js-runtime or impersonate
            # 'js_runtimes': {
            #     'deno': {}
            # },
            # 'impersonate': ImpersonateTarget.from_str('chrome'),
            # 'http_headers': {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            #     'Accept': '*/*',
            #     'Accept-Language': 'en-US,en;q=0.9',
            # },

            # XXX live-streaming
            # 'hls_use_mpegts': True,              # 使用 mpegts 容器强行写入，提升分片拼接容错
            # 'http_chunk_size': 1048576,          # 显式指定 1MB 传输块，规避 Socket 中途超时
            # 'concurrent_fragment_downloads': 4,
            # 'fragment_retries': 10,
            # 'skip_unavailable_fragments': False,
            # 'file_access_retries': 5,
            # 'retry_sleep_functions': {'fragment': lambda n: 1},

            # XXX only MP4/MKV
            # 'external_downloader': 'aria2c',
            # 'external_downloader_args': aria2c_args.split(),
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'unknown_video')
        ext = info.get('ext', 'mp4')
        safe_title = sanitize_filename(title, restricted=True)
        download_folder = set_download_folder()
        if not download_folder.exists():
            raise FileNotFoundError(f'Download folder does not exist: {download_folder}')
        dir_path = download_folder / safe_title
        os.makedirs(dir_path, exist_ok=True)
    
    safe_name = sanitize_filename(name, restricted=True)
    file_path = dir_path / f'{safe_name}.{ext}'
    logging.info(f'Downloading to {file_path}')

    ydl_opts['outtmpl'] = {'default': str(file_path)}

    logging.info(f"Starting to download {name}")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        logging.info("Download completed successfully.")
    except Exception as e:
        logging.error(f"Download failed with exception: {e}")


@lru_cache(maxsize=None)
def cached_video_links_generator(file_path):
    """Generator function to yield name and link from a tab-separated CSV file."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as video_links:
        links_reader = csv.DictReader(video_links)
        # links_reader = csv.DictReader(video_links, delimiter='\t')
        return list((row['Name'], row['Link']) for row in links_reader)


def video_links_generator(file_path):
    yield from cached_video_links_generator(file_path)


if __name__ == '__main__':
    aria2c_args = '-c -j 16 -x 16'
    video_list = os.path.join(working_dir, 'video.csv')
    for name, url in video_links_generator(video_list):
        download_video(url, name, aria2c_args)
