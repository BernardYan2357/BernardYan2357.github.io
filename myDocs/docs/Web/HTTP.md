# HTTP

References: 
- [HTTP | MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)
- [理解HTTP，手搓一个API | BiliBili](https://www.bilibili.com/video/BV1jzKK6aExw)

**超文本传输协议**（HTTP）是一个用于传输超媒体文档（例如 HTML）的[应用层](https://zh.wikipedia.org/wiki/应用层)协议。它是为 Web 浏览器与 Web 服务器之间的通信而设计的

- HTTP 遵循经典的[客户端—服务端模型](https://zh.wikipedia.org/wiki/客户端-服务器架构)，客户端打开一个连接以发出请求，然后等待直到收到服务器端响应
- HTTP 是[无状态协议](https://zh.wikipedia.org/wiki/无状态协议)，这意味着服务器不会在两个请求之间保留任何数据（状态），可以理解为是“无记忆的”

![[Pasted image 20260815164012.png]]

一个完整的网页文档通常由文本、布局描述、图片、视频、脚本等资源构成，客户端与服务端之间通过交换一个个独立的消息（而非数据流）进行通信。由客户端发出的消息被称作请求（request），由服务端发出的应答消息被称作响应（response）

## HTTP 报文

服务端客户端交换的消息称为报文。有两种 HTTP 报文的类型，请求与响应

### Request

HTTP Request 由**请求行（Request Line）、请求头（Headers）、请求体（Body）** 三部分组成：

```http
POST /api/users HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Content-Type: application/json
Content-Length: 27

{"name": "Alice", "age": 25}
```

最后一行空行之前是请求头和请求行，空行之后是请求体

请求行的完整格式为：`方法 路径 版本`：

| 组成                   | 含义          | 示例           |
| -------------------- | ----------- | ------------ |
| HTTP 请求方法（Method）    | 告诉服务器要做什么操作 | `POST`       |
| 请求目标（Request Target） | 资源路径（URI）   | `/api/users` |
| HTTP 版本（Version）     | 协议版本号       | `HTTP/1.1`   |
| 分隔符                  | 各部分之间用空格隔开  | ` `          |

请求方法的单词描述了请求的“意图”，详细信息参考[HTTP 请求方法 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Methods)，常见的请求方法有：

- `GET` 方法用于向服务端请求内容，通常不带请求体
- `POST` 方法用于向服务端提交内容请求处理
- `DELETE` 方法用于请求服务端删除某些内容

请求头的格式为每行一个 `字段名: 值` 键值对：

| 头部字段             | 含义          | 示例值                           |
| ---------------- | ----------- | ----------------------------- |
| `Host`           | 服务器域名和端口    | `example.com`                 |
| `Content-Type`   | 请求体的媒体类型    | `application/json`            |
| `Content-Length` | 请求体的字节长度    | `27`                          |
| `User-Agent`     | 客户端标识       | `Mozilla/5.0`                 |
| `Accept`         | 客户端能接受的响应类型 | `text/html, application/json` |
| `Authorization`  | 认证凭证        | `Bearer eyJhbGciOi...`        |
| `Cookie`         | 会话状态信息      | `sessionId=abc123`            |

请求体，非必需：

| 特征    | 说明                                        |
| ----- | ----------------------------------------- |
| 是否存在  | 通常是 `POST`、`PUT`、`PATCH` 等方法携带，`GET` 一般没有 |
| 格式    | 由 `Content-Type` 决定，常见有 JSON、表单数据、纯文本等    |
| 与头部分隔 | 请求头和请求体之间必须有一个**空行**                      |

| 常见格式 | Content-Type                        | 示例                  |
| ---- | ----------------------------------- | ------------------- |
| JSON | `application/json`                  | `{"name": "Alice"}` |
| 表单数据 | `application/x-www-form-urlencoded` | `name=Alice&age=25` |
| 纯文本  | `text/plain`                        | `Hello, Server`     |

### Response

HTTP Response 由**状态行（Status Line）、响应头（Headers）、响应体（Body）** 三部分组成：

```http
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html
Content-Length: 88

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
```

空行之前是状态行和响应头，空行之后是响应体

状态行的完整格式为：`版本 状态码 原因短语`：

| 组成                  | 含义             | 示例         |
| ------------------- | -------------- | ---------- |
| HTTP 版本（Version）    | 协议版本号          | `HTTP/1.1` |
| 状态码（Status Code）    | 三位数字，表示请求的处理结果 | `200`      |
| 原因短语（Reason Phrase） | 状态码的文字描述       | `OK`       |
| 分隔符                 | 各部分之间用空格隔开     | ` `        |

HTTP响应状态码的分类，详细信息参考[HTTP 响应状态码 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Status)：

| 分类    | 范围    | 含义           | 常见示例                                                  |
| ----- | ----- | ------------ | ----------------------------------------------------- |
| 信息性   | `1xx` | 请求已接收，继续处理   | `100 Continue`                                        |
| 成功    | `2xx` | 请求成功处理       | `200 OK`、`201 Created`                                |
| 重定向   | `3xx` | 需要进一步操作完成请求  | `301 Moved Permanently`、`304 Not Modified`            |
| 客户端错误 | `4xx` | 请求有误，服务器无法处理 | `400 Bad Request`、`404 Not Found`                     |
| 服务器错误 | `5xx` | 服务器内部出错      | `500 Internal Server Error`、`503 Service Unavailable` |

响应头的格式为每行一个 `字段名: 值` 键值对：

| 头部字段             | 含义                   | 示例值                             |
| ---------------- | -------------------- | ------------------------------- |
| `Content-Type`   | 响应体的媒体类型             | `text/html; charset=utf-8`      |
| `Content-Length` | 响应体的字节长度             | `88`                            |
| `Date`           | 服务器生成响应的日期时间         | `Mon, 27 Jul 2009 12:28:53 GMT` |
| `Server`         | 服务器软件信息              | `nginx/1.24.0`                  |
| `Location`       | 重定向的目标 URL（配合 `3xx`） | `/new-location`                 |
| `Set-Cookie`     | 让客户端保存的 Cookie       | `sessionId=abc123; Path=/`      |
| `Cache-Control`  | 缓存策略                 | `no-cache, max-age=3600`        |

响应体，非必需：

| 特征    | 说明                                               |
| ----- | ------------------------------------------------ |
| 是否存在  | 成功响应通常携带，`204 No Content`、`304 Not Modified` 等没有 |
| 格式    | 由 `Content-Type` 决定，常见有 HTML、JSON、纯文本、二进制等       |
| 与头部分隔 | 响应头和响应体之间必须有一个**空行**                             |

| 常见格式 | Content-Type               | 示例                             |
| ---- | -------------------------- | ------------------------------ |
| JSON | `application/json`         | `{"message": "Hello, World!"}` |
| HTML | `text/html`                | `<h1>Hello, World!</h1>`       |
| 纯文本  | `text/plain`               | `Hello, World`                 |
| 二进制  | `application/octet-stream` | 文件下载内容                         |

### curl

使用命令行工具 curl 进行实验：

```bash
curl -v baidu.com # -v 显示详细信息
* Host baidu.com:80 was resolved. # #号为curl的debug信息
* IPv6: (none)
* IPv4: 124.237.177.164, 110.242.74.102, 111.63.65.103, 111.63.65.247
*   Trying 124.237.177.164:80...
* Connected to baidu.com (124.237.177.164) port 80
* using HTTP/1.x
> GET / HTTP/1.1 # 请求行
> Host: baidu.com # 请求头
> User-Agent: curl/8.12.1
> Accept: */* # 通配符，可以接收任意类型
> # 无请求体
* Request completely sent off
< HTTP/1.1 301 Moved Permanently # 状态行
< Location: https://www.baidu.com/ # 重定向的目标 URL
< Date: Sat, 15 Aug 2026 09:29:23 GMT
< Content-Length: 57
< Content-Type: text/html; charset=utf-8
<
<a href="https://www.baidu.com/">Moved Permanently</a>. # 响应体，html

* Connection #0 to host baidu.com left intact
```

还可以调用 deepseek API，体验 POST 请求（请求方法会由 curl 自动指定）：

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \ # 请求头
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": false
      }' # 请求体
```