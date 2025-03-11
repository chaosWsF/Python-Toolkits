## Using yt-dlp+aria2c

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 8 -x 1"`

If cookies are required, 

`yt-dlp <m3u8_URL> --cookies-from-browser firefox --downloader aria2c --downloader-args "-c -j 8 -x 1"`

For livestream, 

`yt-dlp --downloader ffmpeg --hls-use-mpegts <m3u8_URL>`

### Some Problems
The m3u8 playlist hides video streams inside PNGs: [more](https://github.com/yt-dlp/yt-dlp/issues/4381)
