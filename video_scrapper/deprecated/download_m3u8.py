import argparse
import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename
from tqdm import tqdm


class MyLogger:
    """Custom logger class to capture messages"""
    def __init__(self):
        self.messages = []

    def debug(self, msg):
        pass    # Ignore debug messages

    def warning(self, msg):
        self.messages.append(msg)

    def error(self, msg):
        self.messages.append(msg)


def progress_hook(d):
    """Progress hook for the progress bar"""
    if d['status'] == 'downloading':
        fragment_index = d.get('fragment_index', 0)
        total_fragments = d.get('total_fragments', 0)
        if total_fragments:
            pbar.total = total_fragments
            pbar.n = fragment_index
            pbar.refresh()

parser = argparse.ArgumentParser(description="Download m3u8 with yt-dlp and aria2c")
parser.add_argument('url', help='m3u8 URL')
parser.add_argument('--aria2c-args', help='Arguments for aria2c', 
                    default='-c -j 16 -x 16 --summary-interval=0')
args = parser.parse_args()

ydl_opts = {
    'logger': MyLogger(),
    'progress_hooks': [progress_hook],
    'external_downloader': 'aria2c',
    'external_downloader_args': args.aria2c_args.split(),
    # Optional: 'quiet': True  # Uncomment to suppress yt-dlp info logs
}

with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(args.url, download=False)
    title = info['title']   
    safe_title = sanitize_filename(title, restricted=True)    # Sanitize title to ensure it’s a valid folder name
    dir_path = os.path.join('D:\\', 'Saved', 'Videos', safe_title)    # [ ] Consider to use ENV or config file for different OS
    os.makedirs(dir_path, exist_ok=True)
    ydl.params['outtmpl'] = os.path.join(dir_path, '%(title)s.%(ext)s')

pbar = tqdm(desc="Downloading")
print(f"Starting download from: {args.url}")

try:
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])
    
    print("Download completed successfully.")
except Exception as e:
    print(f"Download failed with exception: {e}")
finally:
    pbar.close()

logger = ydl_opts['logger']
if logger.messages:
    print("\nMessages:")
    for i, msg in enumerate(logger.messages, 1):
        print(f"{i}. {msg}")
