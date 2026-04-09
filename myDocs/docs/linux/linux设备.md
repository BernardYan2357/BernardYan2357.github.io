# linux 设备

## 设备文件

## 设备树

## 使用摄像头

## 使用音频设备

aplay 是 ALSA（Advanced Linux Sound Architecture）提供的一个命令行工具，用于播放音频文件

查看音频设备
```bash
lsusb # 查看 USB 设备,观察外接的音频设备是否被系统识别
cat /proc/asound/cards  # 如果你的系统有 /proc/asound/cards 路径,说明 ALSA 驱动已经使用上,可查看 sound devices
arecord -l # 查看音频输入设备
aplay -l  # 查看音频输出设备
    -L # 查看音频设备的详细信息
```

播放音频文件
```bash
aplay -D <设备名称> your-audio-file.wav # 使用指定设备播放音频文件
# 设备名称通过aplay -L命令查看，例如：hw:AudioPCI
alsamixer # 调整音量
```