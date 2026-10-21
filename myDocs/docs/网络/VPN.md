# VPN

**虚拟私人网络**（英语：**V**irtual **P**rivate **N**etwork）将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样

VPN是通过使用专用线路或在现有网络上使用隧道协议建立一个虚拟的点对点连接而形成的

## 配置 docker-easyconnect

不愿意 easyconnect 污染你的电脑？那就用 [docker-easyconnect](https://github.com/docker-easyconnect/docker-easyconnect)

在 WSL 中安装 docker：

```bash
curl -fsSL https://get.docker.com -o install-docker.sh
bash install-docker.sh
```

启动容器：

```bash
docker run -d \
--name vpn \
--device /dev/net/tun \ # 为容器创建虚拟网卡所必需
--cap-add NET_ADMIN \ # 为容器创建虚拟网卡所必需
-p 127.0.0.1:1080:1080 \ # 将容器的1080端口映射到WSL2的127.0.0.1的1080端口，使用SOCKS5协议
-p 127.0.0.1:8888:8888 \ # 使用HTTP/HTTPS协议
-e EC_VER=7.6.7 \ # 指定 EasyConnect 版本
-e CLI_OPTS="-d <VPN服务器地址> -u <用户名> -p <密码>" \
hagb/docker-easyconnect:cli # 首次启动时会自动从云端下载镜像
```

下载镜像超时，原因是 WSL 的镜像模式带来的主机端代理，通常只对 shell 进程及它启动的子进程生效，不会自动传给已经独立运行的 Docker daemon，需要单独为其配置代理

```bash
sudo mkdir -p docker.service.d && printf '%s\n' '[Service]' 'Environment="HTTP_PROXY=http://127.0.0.1:10808"' 'Environment="HTTPS_PROXY=http://127.0.0.1:10808"' 'Environment="NO_PROXY=localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"' | sudo tee proxy.conf >/dev/null

sudo systemctl daemon-reload && sudo systemctl restart docker
```

启动后测试：

```bash
curl -x socks5://127.0.0.1:1080 http://xk.suda.edu.cn
```

### 浏览器访问内网网址

在浏览器中安装 Zero Omega 插件，配置校园网情景：

![[Zero Omega.png]]

同时配置 auto switch，设置域名匹配 `*.suda.edu.cn` 时使用校园网情景（使用一段时间才发现 auto switch 无法设置默认情景模式为系统代理，这样在默认情况下直接覆盖掉全局代理，所有网页都走直连了，搞不懂🫠，还是手动切换情景吧）

### 连接内网服务器

新建一个容器：

```bash
docker run -d \
--name vpn_ssh \
--device /dev/net/tun \ # 为容器创建虚拟网卡所必需
--cap-add NET_ADMIN \ # 为容器创建虚拟网卡所必需
-p 127.0.0.1:1080:1080 \ # 将容器的1080端口映射到WSL2的127.0.0.1的1080端口，使用SOCKS5协议
-p 127.0.0.1:8888:8888 \ # 同上，使用HTTP/HTTPS协议
-p 127.0.0.1:2222:2222 \ # 将容器2222端口发布出来
-e EC_VER=7.6.7 \ # 指定 EasyConnect 版本
-e CLI_OPTS="-d <VPN服务器地址> -u <用户名> -p <密码>" \
-e FORWARD="2222:<内网服务器ip>:22" \ # 起端口转发作用，将内网服务器的22端口转发到本地2222端口
hagb/docker-easyconnect:cli # 首次启动时会自动从云端下载镜像
```

进入容器并下载 openssh-server

