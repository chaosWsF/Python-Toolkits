import argparse
import yt_dlp
from tqdm import tqdm


class MyLogger:
    def __init__(self):
        self.messages = []
    def debug(self, msg):
        pass
    def warning(self, msg):
        self.messages.append(msg)
    def error(self, msg):
        self.messages.append(msg)


def progress_hook(d):
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
                    default='-c -j 16 -x 1 --summary-interval=0')
args = parser.parse_args()

pbar = tqdm(desc="Downloading")
logger = MyLogger()
ydl_opts = {
    'logger': logger,
    'progress_hooks': [progress_hook],
    'external_downloader': 'aria2c',
    'external_downloader_args': args.aria2c_args.split(),
    # Optional: 'quiet': True  # Uncomment to suppress yt-dlp info logs
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])
except Exception as e:
    print(f"Download failed with exception: {e}")
finally:
    pbar.close()
    if logger.messages:
        print("\nCaptured messages:")
        for msg in logger.messages:
            print(msg)
