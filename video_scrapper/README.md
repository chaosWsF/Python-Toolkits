## Using yt-dlp+aria2c

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 16 -x 1"`

Hiding miscellaneous outputs from aria2 

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 8 -x 1 --summary-interval=0"`

If cookies are required, 

`yt-dlp <m3u8_URL> --cookies-from-browser firefox --downloader aria2c --downloader-args "-c -j 16 -x 1"`

For livestream, 

`yt-dlp --downloader ffmpeg --hls-use-mpegts <m3u8_URL>`

### Some Problems

The m3u8 playlist hides video streams inside PNGs: [more](https://github.com/yt-dlp/yt-dlp/issues/4381)

### Tools

1. Adding the tool `app.py` built by Flask as webUI that 

   + has a bar of the download progress and the percentage of downloaded part
   + has a log section to catch exception and other outputs, enumerating them (1,2,3,...)
   + has a input bar to accept aria2c arguments
   + makes a folder for downloaded files under ~/Downloads/Videos, which needs to check folder existence

   **Limits**: 
   
   + It does not work for live stream.
