# Web 应用开发

References: - [MDN Web 文档 | mozilla](https://developer.mozilla.org/zh-CN/docs/MDN/Tutorials)

## 一些概念

Vibe Coding 时代，能够精准描述自己的需求尤为重要，要想描述需求，一些基本概念和常用术语必须掌握

有用的链接：[VibeCoding术语课 | ZTough](https://space.bilibili.com/42484832/lists/8995110?type=season)

### NPM

```bash
npm install -g <包名> --registry=https://registry.npmmirror.com
npm cache clean --force # 清理缓存
npm cache verify
```

## JavaScript

JavaScript 由代码和宿主环境两部分组成，宿主环境包括浏览器和 node

BOM 是指浏览器对象模型，DOM 是指文档对象模型，它们是浏览器作为宿主环境时所提供的与环境交互必须的扩展，BOM 代表整个浏览器，DOM 代表浏览器页面上展示的内容

## Chrome 插件开发

- [浏览器插件开发](https://www.fengfengzhidao.com/special/7/81)

### 最小示例

文件结构：

```bash
my_extension/
├── manifest.json # 插件的配置文件，必须包含
├── /assets
│   └── icon.png
├── popup.html # 插件的弹出页面
├── popup.js # 插件的脚本文件
```

manifest.json：

```json
{
    "manifest_version": 3,
    "name": "我的插件",
    "version": "0.0.1",
    "description": "学习chrome插件开发",
    "author": "MuYun",
    "action": {
        "default_icon": {
            "16": "assets/icon16.png",
            "32": "assets/icon32.png",
            "48": "assets/icon48.png",
            "64": "assets/icon64.png",
            "128": "assets/icon128.png"
        },
        "default_popup": "popup.html"
    },
    "icons": {
        "16": "assets/icon16.png",
        "32": "assets/icon32.png",
        "48": "assets/icon48.png",
        "64": "assets/icon64.png",
        "128": "assets/icon128.png"
    }
}
```
- action：定义插件的图标`default_icon`和点击图标时显示的页面`default_popup`
- icons：定义用于 Chrome 扩展管理页面、扩展商店列表、扩展详情页等地方显示的扩展图标

popup.html：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <!-- title标签实际并不会显示 -->
    <title>title</title>
</head>
<body style="width: 200px; height: 124px;">
    <h1>Hello World!</h1>
</body>
</html>
```

### Content Script

content script 是运行在网页上下文（DOM）中的 JavaScript 脚本，由浏览器扩展注入，能访问网页的 DOM 结构，但和网页自身的脚本、扩展的后台脚本（background）有严格的隔离

- 能读写当前网页的 DOM，修改样式、文本、节点等
- 不能访问网页自身的全局变量 / 函数
- 不能直接访问扩展的 chrome.api 全部方法（仅能访问 chrome.runtime、chrome.storage 等少数 API）
- 可通过 chrome.runtime.sendMessage 与扩展的后台脚本通信

要使用 content script，需要在 manifest.json 中声明：

```json
"content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": [],
      "run_at": "document_end"
    }
  ]
```

- matches：指定在哪些页面注入 content script，`<all_urls>` 表示所有页面，也可以使用 URL 匹配特定页面，由于 "content_scripts" 声明为数组，因此可以配置多个 content script 注入不同的页面，例如：["https://blog.csdn.net/*"] 其它匹配规则示例：
  - "exclude_matches": ["https://example.com/*"]，排除的URL
  - "include_globs": ["*example.com/*/test*"]，使用glob规则匹配要注入的URL
  - "exclude_globs": ["*example.com/*/test/old*"]，排除的glob规则
- js：要注入的 JavaScript 文件列表
- css：要注入的 CSS 文件列表
- run_at：指定注入时机，`document_end` 表示在 DOM 加载完成后注入（也可选 `document_start` 或 `document_idle`）
- all_frames：是否在所有框架（iframe）中注入，默认为 false 仅注入顶层页面
- match_about_blank：是否在 about:blank 页面中注入，默认为 false
- world：指定 content script 运行的环境，默认为 "ISOLATED"，表示在隔离环境中运行，无法访问网页自身的 JavaScript 变量和函数；如果设置为 "MAIN"，则在网页的主上下文中运行

content script 的核心能力是操作网页 DOM，可以修改网页标题、插入元素、修改样式等。例如：

```javascript
console.log("Content Script注入成功!");
// 修改网页标题
document.title = "被Content Script修改后的标题";
// 向网页插入一个元素
const div = document.createElement("div");
div.style.cssText = "position:fixed;top:0;left:0;background:blue;color:white;padding:10px;z-index:9999;";
div.innerText = "这是Content Script插入的内容";
document.body.appendChild(div);
```
