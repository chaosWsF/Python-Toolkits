# Online Video Scrapper

## Using yt-dlp+aria2c for m3u8

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 16 -x 1"`

Handling miscellaneous outputs from aria2 via 

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 8 -x 1 --summary-interval=1 --console-log-level=info"`

If cookies are required, 

`yt-dlp <m3u8_URL> --cookies-from-browser firefox --downloader aria2c --downloader-args "-c -j 12 -x 1"`

For live stream, 

`yt-dlp --downloader ffmpeg --hls-use-mpegts <m3u8_URL>`

### Problems

The m3u8 playlist hides video streams inside PNGs: [detail](https://github.com/yt-dlp/yt-dlp/issues/4381)

### Tools

1. Tried formatting outputs of YoutubeDL in `deprecated/download_m3u8.py`
2. Adding the tool `app.py` built by Flask as webUI that 
   + has a bar of the download progress and the percentage of downloaded part
   + has a log section to catch exception and other outputs, enumerating them (1,2,3,...)
   + has a input bar to accept aria2c arguments
   + makes a folder for downloaded files under ~/Downloads/Videos, which needs to check folder existence
