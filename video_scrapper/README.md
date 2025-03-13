# Online Video Scrapper

## Using yt-dlp+aria2c for m3u8

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 8 -x 1"`

Handling miscellaneous outputs from aria2 via 

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 16 -x 1 --summary-interval=1 --console-log-level=info"`

If cookies are required, 

`yt-dlp <m3u8_URL> --cookies-from-browser firefox --downloader aria2c --downloader-args "-c -j 12 -x 1"`

For live stream, 

`yt-dlp --downloader ffmpeg --hls-use-mpegts <m3u8_URL>`

### Tools

1. Tried formatting outputs of YoutubeDL in `deprecated/download_m3u8.py`
2. Added `app.py` built by Flask as webUI that 
   + has a bar of the download progress and the percentage of downloaded part
   + has a log section to catch exception and other outputs, enumerating them (1,2,3,...)
   + has a input bar to accept aria2c arguments
   + makes a folder for downloaded files under ~/Downloads/Videos, which needs to check folder existence
3. Added `simple_downloader.py` for batch downloading with provided list of links

### Problems

The m3u8 playlist hides video streams inside PNGs: [detail](https://github.com/yt-dlp/yt-dlp/issues/4381)

**Checking video with `ffmpeg`**

#### Step 1: Basic File Info with `ffprobe`
`ffprobe` (bundled with FFmpeg) is your go-to for analyzing media files. It’ll give you detailed metadata about the video, audio, and container, which can reveal if something’s broken.

- **Command**:
  ```bash
  ffprobe -i yourvideo.mp4 -show_streams -show_format -print_format json
  ```
- **What It Does**:
  - `-i yourvideo.mp4`: Specifies your input file (replace "yourvideo.mp4" with the actual filename).
  - `-show_streams`: Displays info about video, audio, and other streams.
  - `-show_format`: Shows container details (like duration, bitrate).
  - `-print_format json`: Outputs in JSON for easier reading (optional; remove it for plain text).
- **What to Look For**:
  - **Duration**: Check if it matches the expected length (not 0:10). If it’s wrong or missing, the file might be truncated or have a broken header.
  - **Codec Info**: Look at `codec_name` (e.g., `h264` for video, `aac` for audio). Unsupported or mismatched codecs could confuse VLC.
  - **Stream Count**: Ensure there’s at least one video and audio stream. Missing streams might indicate corruption.


#### Step 2: Check for Errors During Playback
To dig deeper, try running FFmpeg to "play" the file (without re-encoding) and log any errors.

- **Command**:
  ```bash
  ffmpeg -i yourvideo.mp4 -f null - > log.txt 2>&1
  ```
- **What It Does**:
  - `-i yourvideo.mp4`: Input file.
  - `-f null -`: Outputs to a null sink (no actual file written, just analysis).
  - `> log.txt 2>&1`: Redirects output and errors to a text file.
- **What to Look For**:
  - Open `log.txt` and search for terms like "error," "corrupt," "invalid," or "missing." For example:
    - `Invalid data found when processing input`: Suggests a broken file.
    - `moov atom not found`: The MP4 header is missing or misplaced (common with interrupted downloads/recordings).
    - `frame size does not match`: Encoding issue or corruption mid-file.

#### Step 3: Test Remuxing to Diagnose/Fix
If the file seems intact but VLC can’t handle it, the container might be the issue. Remuxing with FFmpeg copies the streams into a new MP4 without re-encoding, which can fix header or indexing problems.

- **Command**:
  ```bash
  ffmpeg -i yourvideo.mp4 -c copy -map 0 newvideo.mp4
  ```
- **What It Does**:
  - `-c copy`: Copies video/audio streams without re-encoding (fast).
  - `-map 0`: Includes all streams from the input.
  - `newvideo.mp4`: Output file.
- **Next Step**: Try opening `newvideo.mp4` in VLC. If it works, the original container was likely borked. If it still fails, the streams themselves might be damaged.

#### Step 4: Look for Truncation or Corruption
Since it’s a 2GB file with a 0:10 duration, it might be truncated (e.g., a download cut off early). Compare the file size to the expected size (if you know it). FFmpeg can also estimate if data’s missing:

- **Command**:
  ```bash
  ffprobe -i yourvideo.mp4 -count_frames -show_entries stream=nb_read_frames
  ```
- **What to Look For**: If `nb_read_frames` is absurdly low (e.g., a few hundred for a supposed long video), the file’s incomplete or unreadable beyond a point.
