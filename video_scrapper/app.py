from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename
import traceback

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure key
socketio = SocketIO(app)

# Global variables to track progress and logs
progress_data = {'progress': 0, 'logs': []}
download_thread = None


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
    global progress_data
    if d['status'] == 'downloading':
        fragment_index = d.get('fragment_index', 0)
        total_fragments = d.get('total_fragments', 0)
        if total_fragments:
            progress = int((fragment_index / total_fragments) * 100)
            progress_data['progress'] = progress
            socketio.emit('progress_update', {'progress': progress})


def download_video(url, aria2c_args):
    """Download function to download video from URL"""
    global progress_data
    progress_data['progress'] = 0
    progress_data['logs'] = []

    logger = MyLogger()
    ydl_opts = {
        'logger': logger,
        'progress_hooks': [progress_hook],
        'external_downloader': 'aria2c',
        'external_downloader_args': aria2c_args.split(),
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            safe_title = sanitize_filename(title, restricted=True)
            dir_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'Videos', safe_title)
            os.makedirs(dir_path, exist_ok=True)
            ydl.params['outtmpl'] = os.path.join(dir_path, '%(title)s.%(ext)s')
            
            ydl.download([url])
        
        progress_data['logs'].append("Download completed successfully.")
    except Exception as e:
        progress_data['logs'].append(f"Download failed with exception: {str(e)}")
        progress_data['logs'].append(traceback.format_exc())
    finally:
        progress_data['progress'] = 100
        socketio.emit('progress_update', {'progress': 100})
        socketio.emit('logs_update', {'logs': progress_data['logs']})


@app.route('/')
def index():
    """Route for the main page"""
    return render_template('index.html')


@app.route('/start_download', methods=['POST'])
def start_download():
    """Route to start the download process"""
    global download_thread
    if download_thread and download_thread.is_alive():
        return jsonify({'status': 'error', 'message': 'Download already in progress'})
    
    url = request.form['url']
    aria2c_args = request.form['aria2c_args']
    download_thread = threading.Thread(target=download_video, args=(url, aria2c_args))
    download_thread.start()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
