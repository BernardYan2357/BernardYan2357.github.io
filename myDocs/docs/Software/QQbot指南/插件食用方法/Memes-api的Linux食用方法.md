# Memes-api的Linux食用方法

## QQbot连接方式的选择

本指南采用napcat🐱+koishi的方式连接。

> 若使用QQ开放平台连接，机器人将无法获取用户头像，memes-generater的大部分功能将无法使用。

### 部署koishi

#### 推荐方式：1Panel应用商店下载😍

##### 下载插件：memes-api

koishi插件市场搜索*memes-api*,下载。

##### Docker部署

```bash
sudo docker run -d \
  --name=meme-generator \
  -p 2233:2233 \
  --restart always \
  meetwq/meme-generator:latest
```

> 源网址：[Docker 部署 · Meme Crafters/meme-generator Wiki](https://github.com/MemeCrafters/meme-generator/wiki/Docker-%E9%83%A8%E7%BD%B2)

- 完整的配置命令

- ```bash
  docker run -d \
    --name=meme-generator \
    -p 2233:2233 \
    --restart always \
    -v <YOUR_DATA_DIR>:/data \ #此处<YOUR_DATA_DIR>应替换为实际路径，例如替换为/var/lib/meme-generator
    -e MEME_DIRS='["/data/memes"]' \ #额外表情路径,默认为“/data/memes"
    -e MEME_DISABLED_LIST='[]' \ #禁用表情列表
    -e GIF_MAX_SIZE=10.0 \ #限制生成的 gif 文件大小
    -e GIF_MAX_FRAMES=100 \ #限制生成的 gif 文件帧数
    -e BAIDU_TRANS_APPID=<YOUR_BAIDU_TRANS_APPID> \ #百度翻译 appid
    -e BAIDU_TRANS_APIKEY=<YOUR_BAIDU_TRANS_APIKEY> \ #百度翻译 apikey
    -e LOG_LEVEL='INFO' \ #日志等级
    meetwq/meme-generator:main
  ```

##### 建立Docker网络

将koishi与memes-api通过网络连接

```bash
sudo docker network create my_network #建立Bridge网络(默认网络)
sudo docker network connect my_network container_name_or_id
```

查询Docker容器id命令:

```bash
docker ps #列出所有正在运行的容器及其 ID
docker ps -a #列出所有容器（包括已停止的容器）及其 ID
docker ps -a --format "{{.ID}}" #仅显示容器 ID
```

###### Docker网络相关命令

查看Docker网络：

```bash
docker network ls
```

```bash
docker network inspect a1b2c3d4e5f6  # 通过网络ID或名称查看详细信息
```

删除Docker网络：

```bash
docker network rm <network_name_or_id>
```

- **注意！** 如果网络正在被容器使用，Docker 会拒绝删除。需要先删除使用该网络的容器，然后再删除网络。
  
  删除Docker容器：
  
  ```bash
  docker rm -f <container_name_or_id>
  ```

#### 填写配置

在`memes-api`插件配置处，将请求地址改为http://`服务器IP（最好是私网IP）`：`2233`

记得开放2233端口

#### 启动memes-api插件

在koishi控制面板启动插件，观察是否加载成功。

#### 额外表情列表加载

**下载Git** 命令如下：

```bash
sudo apt update
sudo apt install git
git --version #查看是否下载成功
```

**Clone`Git`仓库**

找一个地址存放额外表情文件，终端进入该文件夹：

```bash
cd /var/lib/memes-generator
git clone --depth=1 https://github.com/MemeCrafters/meme-generator-contrib
# git clone：Git 命令，用于克隆（下载）一个远程仓库到本地。
# --depth=1：指定克隆的深度为 1，即只克隆最新的提交历史，不包含完整的提交记录。
# https://github.com/MemeCrafters/meme-generator-contrib：远程仓库的 URL，表示要克隆的仓库地址。
cd #返回home目录
```

> **将表情文件移动至主表情库（推荐方式）**

主表情文件夹一般在`/var/lib/docker/overlay2/一串数字和字母组合/diff/app/meme_generator/memes`

- `/var/lib/docker/overlay2/`解释：Docker 容器的文件系统由以下几部分组成：
  
  - **镜像层（Image Layers）**：只读层，包含容器的基础文件系统。`/var/lib/docker/overlay2/`
  
  - **容器层（Container Layer）**：可写层，存储容器运行时的修改（如新建文件、修改文件）。`/var/lib/docker/containers/<容器ID>/`
  
  - **挂载的卷（Volumes/Bind Mounts）**：外部挂载的目录或卷，用于持久化数据。
    表情文件存储在镜像层

- 一串数字和字母组合是 Docker 使用的 **Overlay2 存储驱动** 生成的 **层 ID**
  
  - ```text
    /var/lib/docker/overlay2/
      ├── <层ID>/
      │   ├── diff/        # 该层的文件内容
      │   ├── link         # 指向该层的符号链接
      │   ├── lower        # 该层依赖的下层
      │   └── merged/      # 该层与其他层合并后的文件系统（用于容器运行时）
      └── l/               # 包含层 ID 的符号链接
    ```
  
  如果容器太多，一个一个找显然太麻烦，可以使用以下命令获取meme-generator的层id：

```bash
    #输入
    docker inspect --format '{{.GraphDriver.Data.UpperDir}}' <容器ID或名称>
    #输出
    /var/lib/docker/overlay2/093c4cf31dcc03d7a3fe5f62b7113f4a9e4c6e9626701d3cff6a93cf1da6edd3/diff
    #"093c4cf31dcc03d7a3fe5f62b7113f4a9e4c6e9626701d3cff6a93cf1da6edd3"即为层id
```

找到文件夹后，将额外表情粘贴至此。重启容器，重启插件，若成功加载出293个表情，说明成功了。（后续已更新，不止293）

> **官方给的方法，但是给的是Windows系统演示，Linux系统我没弄成，可能docker需要额外步骤。**

  [koishi memes-api 插件配置指南](https://www.bilibili.com/video/BV1JEqhYQEN8/?share_source=copy_web&vd_source=835d8dc1e227680f14032bd463441428/)

### 附录：meme-generator配置文件路径

配置文件不会自动生成

默认配置文件位置：

- Windows: `C:\Users\<username>\AppData\Roaming\meme_generator\config.toml`
- Linux: `~/.config/meme_generator/config.toml`
