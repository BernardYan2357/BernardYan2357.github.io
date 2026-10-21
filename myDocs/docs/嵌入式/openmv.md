# 从零开始的openmv学习之路

参考：

- [OpenMV官网](https://openmv.io/)
- [OpenMV Github仓库](https://github.com/openmv)
- [OpenMV官方文档](https://docs.openmv.io/)
- [OpenMV官方文档(中文翻译)](https://docs.singtown.com/micropython/zh/latest/openmvcam/index.html)
- [OpenMV中文教程](https://book.openmv.cc/index.html)
- [OpenMV快速上手](https://blog.csdn.net/Mculover666/article/details/129778144)

## 机器视觉界的“Arduino”

- OpenMV是一个开源项目，是一款低价、可扩展、使用microPython编程的机器视觉摄像头模组
- 常见的版本是OpenMV4，主控和摄像头使用：STM32H743VIT6 + OV7725，该版本摄像头模组可更换
- 有子版本：base（常见名：openmv4 h750）、plus（常见名：openmv4 h7 Plus）

## DIY一块OpenMV

- [官方硬件开源在GitHub](https://github.com/openmv/openmv-boards)
- [立创开源广场开源openmv h750](https://oshwhub.com/affinelab/openmv4h750)
- [立创开源广场开源openmv h7 Plus](https://oshwhub.com/affinelab/openmv4_plus)

没有能力不要轻易尝试DIY！血的教训🥲

## 搭建开发环境

OpenMV IDE是用于OpenMV Cam的集成开发环境，具有强大的文本编辑器，调试终端和带有直方图显示的帧缓冲区查看器
[下载](https://github.com/openmv/openmv-ide)
