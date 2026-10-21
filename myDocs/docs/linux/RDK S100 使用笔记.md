# RDK S100 使用笔记

使用起来真的不太行......

问题集中在：
- 系统存在 BUG
- 性能较差
- 相关资料少，官方资料不够完善，例如没有官方的挂载硬盘教程
- 社区生态还没成熟，不过在论坛问问题会有工作人员回复

## 挂载硬盘

References: [RDK S100 硬盘挂载教程 | 地瓜机器人论坛](https://forum.d-robotics.cc/t/topic/30933)

将提供的 K-RICARD M.2 NVMe SSD(128G) 安装到开发板上

开机，查看是否识别到 NVMe：

```bash
ls /dev/nvme*
```

格式化为 ext4：

```bash
sudo mkfs.ext4 /dev/nvme0n1
```

创建挂载目录并挂载：

```bash
sudo mkdir -p /data # /data 是自定义的名称，一般认为 /mnt 目录专用于临时挂载硬盘
sudo mount /dev/nvme0n1 /data
```

查看挂载是否成功：

```bash
df -h
```

以上为临时挂载，要想持久化看下文：

获取硬盘 UUID：

```bash
lsblk -f
```

编辑 `/etc/fstab`：

```bash
sudo nano /etc/fstab
```

在末尾添加：

```bash
UUID=<NVMe的UUID> /data ext4 defaults,nofail 0 2 
# nofail 参数可以避免NVMe识别失败时系统因为它卡在开机阶段
```

测试配置是否正确：

```bash
sudo mount -a
df -h /data # 确认挂载
```

这样之后重启系统，NVMe 会自动挂载到 `/data`

## rdkos_info

[rdkos_info | RDK S100/S600 DOC](https://developer.d-robotics.cc/rdk_s_doc/Appendix/rdk-command-manual/cmd_rdkos_info?v=4.0.5&p=RDK+S100)