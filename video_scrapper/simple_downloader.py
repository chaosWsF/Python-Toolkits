import os
import csv
import logging
from functools import lru_cache
from yt_dlp import YoutubeDL
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


def download_video(url, name, aria2c_args):
    """Download function to download video from URL"""
    ydl_opts = {
            'external_downloader': 'aria2c',
            'external_downloader_args': aria2c_args.split(),
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'unknown_video')
        ext = info.get('ext', 'mp4')
        safe_title = sanitize_filename(title, restricted=True)
        dir_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'Videos', safe_title)
        os.makedirs(dir_path, exist_ok=True)
    
    safe_name = sanitize_filename(name, restricted=True)
    file_path = os.path.join(dir_path, f'{safe_name}.{ext}')
    logging.info(f'Downloading to {file_path}')
    ydl_opts['outtmpl'] = {'default': file_path}

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
