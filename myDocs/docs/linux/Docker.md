# Docker

## Docker 安装

```bash
curl -fsSL https://get.docker.com -o install-docker.sh
bash install-docker.sh
```

## Docker 镜像源配置

```bash
sudo nano /etc/docker/daemon.json
```

```bash
{
    "registry-mirrors": [
        "https://docker.1ms.run",
        "https://docker.xuanyuan.me"
    ]
}
```

配置完成后重启docker服务：

```bash
sudo systemctl restart docker
```

## Docker 命令

References: [常用的 Docker 客户端命令](https://www.runoob.com/docker/docker-container-usage.html)

容器命令：

```bash
docker ps
	-a
docker run
docker start
docker logs <name>
docker exec
docker stop
docker rm
```

镜像命令：