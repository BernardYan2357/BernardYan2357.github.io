# Pixluna插件部署

## Pixiv设置

- `pixiv.phpSESSID`的获取
  
  访问 [www.pixiv.net](https://www.pixiv.net) 源站并登录，打开浏览器控制台(f12)，选中`Application`一栏，在 cookie 列表里找到“键(key)”为PHPSESSID的一栏，将它的“值(value)”复制后填写。

## 配置代理

国内服务器大概率不能直连Pixiv,需要使用代理服务器。买台香港服务器（最好不要是国内云服务器提供商的，会查出来代理），具体操作不知道，我没弄过。
