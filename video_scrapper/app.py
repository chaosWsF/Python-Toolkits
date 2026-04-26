import os
import sys
import re
import threading
import traceback
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename

load_dotenv()

secret_key = os.getenv('FLASK_SECRET_KEY')
port = int(os.getenv('FLASK_PORT', 5000))    # Default to 5000 if not set

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
socketio = SocketIO(app)

# Global variables to track progress and logs
progress_data = {'progress': 0, 'logs': [], 'aria2c_output': []}
download_thread = None


class SocketIOStream:
    """Custom stream class to capture output and send it via SocketIO"""
    def __init__(self, socketio):
        self.socketio = socketio
        self.ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')    # Regex for ANSI codes

    def write(self, msg):
        clean_msg = self.ansi_escape.sub('', msg).strip()
        if clean_msg:
            self.socketio.emit('aria2c_output', {'output': clean_msg})

    def flush(self):
        pass


class MyLogger:
    """Custom logger class to capture messages"""
    def __init__(self):
        self.messages = []
        self.aria2c_output = []

    def debug(self, msg):
        pass    # Ignore debug messages

    def warning(self, msg):
        self.messages.append(msg)

    def error(self, msg):
        self.messages.append(msg)
    
    def aria2c_log(self, msg):
        self.aria2c_output.append(msg)
        socketio.emit('aria2c_output', {'output': msg})


def progress_hook(d):
    """Progress hook for the progress bar"""
    global progress_data
    if d['status'] == 'downloading':
        fragment_index = d.get('fragment_index', 0)
        total_fragments = d.get('total_fragments', 0)
        if total_fragments > 0:
            progress = int((fragment_index / total_fragments) * 100)
            progress_data['progress'] = progress
            socketio.emit('progress_update', {'progress': progress})
        else:
            socketio.emit('progress_update', {'progress': 'unknown'})
            print("Progress unknown - total fragments not available")


def download_video(url, aria2c_args):
    """Download function to download video from URL"""
    global progress_data
    progress_data['progress'] = 0
    progress_data['logs'] = []
    progress_data['aria2c_output'] = []

    logger = MyLogger()
    ydl_opts = {
        'logger': logger,
        'progress_hooks': [progress_hook],
        'external_downloader': 'aria2c',
        'external_downloader_args': aria2c_args.split(),
        'verbose': True
    }
    
    output_stream = SocketIOStream(socketio)
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = output_stream
    sys.stderr = output_stream

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'unknown_video')    # Fallback if title is missing
            safe_title = sanitize_filename(title, restricted=True)
            dir_path = os.path.join('D:\\', 'Saved', 'Videos', safe_title)    # [ ] Consider to use ENV or config file for different OS
            os.makedirs(dir_path, exist_ok=True)
        
        ydl_opts['outtmpl'] = {
            'default': os.path.join(dir_path, '%(title)s.%(ext)s')
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
        progress_data['logs'].append("Download completed successfully.")
    except Exception as e:
        progress_data['logs'].append(f"Download failed with exception: {str(e)}")
        progress_data['logs'].append(traceback.format_exc())
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        progress_data['progress'] = 100
        socketio.emit('progress_update', {'progress': 100})
        socketio.emit('aria2c_output', {'output': 'Download finished'})
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
    socketio.run(app, debug=True, port=port)
