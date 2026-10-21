# FFmpeg

references:

- [FFmpeg 教程文档](https://wklchris.github.io/blog/FFmpeg/index.html)

常用命令：

```powershell
ffmpeg -y -i "input.mp3" -i "cover.jpg" -map 0:a -map 1:v -c:a copy -c:v mjpeg -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" "input.cover.tmp.mp3" # 为 mp3 添加封面
```

# MPC-HC

项目地址：[clsid2/mpc-hc: Media Player Classic](https://github.com/clsid2/mpc-hc)

一些有趣的功能：

- You can stream videos directly from Youtube and many other video websites by putting [[Media#YT-DIP]] in the MPC-HC installation folder
	- Then you can open website URLs in the player: Menu > File > Open File/URL  
	- You can even download those videos: Menu > File > Save a copy
	- Several YDL configuration options are found here: Options > Advanced. This includes an option to specify the location of the .exe in case you don't want to put it in MPC-HC folder
	- To be able to download in best quality with yt-dlp, it is recommended to also put ffmpeg.exe in the MPC-HC folder

# YT-DIP

项目地址：[yt-dlp/yt-dlp: A feature-rich command-line audio/video downloader](https://github.com/yt-dlp/yt-dlp)

下载 yt-dlp.exe，将其路径添加到 PATH

通过命令行的方式调用 yt-dlp.exe：

```powershell
yt-dlp -x "video URL" # 只下载视频的音频
```
