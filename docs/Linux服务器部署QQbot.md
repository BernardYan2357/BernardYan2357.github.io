# Linux服务器部署QQbot

本指南采用**Napcat + koishi**方式部署QQ机器人

- NapCat通过魔法✨的手段获得了 QQ 的发送消息、接收消息等接口并把他们以OneBot的规范开放，允许其他组件按照规范进行通信。  [NapCatQQ | 现代化的基于 NTQQ 的 Bot 协议端实现](https://napneko.pages.dev/)
  
  顺便一提，Napcat的控制面板做的真的很好，甚至还能导入网易云歌单听歌😋。

- Koishi 是一个跨平台、可扩展、高性能的聊天机器人框架。[Koishi 古明地恋](https://koishi.chat/zh-CN/)
  
  ---

## 配置Napcat

### Docker部署方式

创建文件`docker-compose.yml`

```yml
# docker-compose.yml
version: "3"
services:
    napcat:
        environment:
            - NAPCAT_UID=${NAPCAT_UID}
            - NAPCAT_GID=${NAPCAT_GID}
        ports:
            - 3000:3000
            - 3001:3001
            - 6099:6099
        container_name: napcat
        network_mode: bridge
        restart: always
        image: mlikiowa/napcat-docker:latest
```

在该目录下执行 `sudo docker-compose up -d` ，如果网络条件良好，过一会就能看到容器启动成功的提示。  

然后浏览器访问：`http://<服务器公网IP>:6099/webui`，记得开放端口。

### QQ登录

手机QQ登录，如果二维码失效，就打开1panel的docker界面，查看napcat日志，扫码登陆。

### Napcat听歌

复制歌单链接，可以看到：`https://music.163.com/playlist?***id=5105017861***&uct2=U2FsdGVkX188EfQzuityIk/NBoLutOYZ69HyjsDr5ys=`，复制id。

点击`其他配置`>`webUI配置`,填写网易云音乐歌单ID。

---

## 配置Koishi

### 下载Koishi

**推荐方式：1Panel应用商店下载😍**
然后浏览器访问：`http://<服务器公网IP>:5140`

### 配置Koishi步骤

- **auth（权限设置）**
  
  - 设置管理员账号（这一步需要你先完成QQbot的连接）：点击auth插件配置，设置账号和密码，启用插件。
    跳转到用户资料界面，填写账密，绑定平台：
    平台：`onebot`, 账号：`你自己的QQ号`
    之后向QQbot发送验证码即可完成绑定。
  - 普通用户权限为1，请在指令管理界面将重要指令权限提高。

- **插件安装**
  - 安装完Koishi，第一步：点开依赖管理，刷新，点击小火箭🚀更新依赖。
    插件市场选择插件添加>安装>点击插件配置>全局配置>添加插件>选择插件>配置参数>保存配置>启用插件。

- **插件市场镜像源配置**
  
  - 如果你无法加载插件市场，或出现“正在加载版本数据”提示，说明你需要更换镜像源了。
  
  - [Koishi 镜像一览 - 技术分享 - Koishi Forum](https://forum.koishi.xyz/t/topic/4000)
  
  - 配置镜像源步骤：点击插件配置，点击插件：`market`
    `registry.endpoint`写入`https://registry.npmmirror.com/`
    `search.endpoint`写入`https://registry.koishi.chat/index.json(可以换成其他的市场镜像)`

---

## 通过onebot适配器连接两组件

koishi插件市场下载`adapter-onebot`

### websocket方式

在Napcat操作面板处，选择网络配置，新建Websocket服务器，`端口号`填写3000，`Token`可填，打开。

在`adapter-onebot`插件配置处，填写Napcat上登录的QQid，`Token`与上文一致，协议选择`ws`,`endpoint`(服务器地址)填写：ws://`<服务器公网IP>`:`端口号(与上文保持一致)`。

保存配置，启动插件，观察运行日志是否出现`2025-03-13 17:36:21 [I] adapter connect to server: ws://<服务器公网IP>:3000/`。若显示，且右下方状态图标变绿,则连接成功。

在QQ向bot发送`status`或`help`,观察是否回复。

### 反向websocket

和websocket差不多，就是反过来。
