## Docker的安装

以ubuntu为例，安装docker的命令如下：

```bash
# 更新apt源并安装依赖
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# 设置 Docker 稳定版仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# 更新apt源并安装Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
# 启动Docker
sudo systemctl start docker
# 验证Docker是否安装成功
docker -v
sudo docker run hello-world
```

## Docker镜像源配置

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

```bash
sudo systemctl restart docker
```
