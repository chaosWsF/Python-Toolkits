## Using yt-dlp+aria2c

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 16 -x 1"`

Hiding miscellaneous outputs from aria2 

`yt-dlp <m3u8_URL> --downloader aria2c --downloader-args "-c -j 16 -x 1 --summary-interval=0"`

If cookies are required, 

`yt-dlp <m3u8_URL> --cookies-from-browser firefox --downloader aria2c --downloader-args "-c -j 16 -x 1"`

For livestream, 

`yt-dlp --downloader ffmpeg --hls-use-mpegts <m3u8_URL>`

### Some Problems

The m3u8 playlist hides video streams inside PNGs: [more](https://github.com/yt-dlp/yt-dlp/issues/4381)

### Features

Adding the tool that

+ has a bar of the download progress and the percentage of downloaded part
+ formats the output in command line, catches exception and other outputs and enumerate them with 1,2,3,...
+ passes aria2c arguments with prasing CLI input
+ makes a folder for downloaded files under ~/Downloads/Videos, which needs to check folder existence
