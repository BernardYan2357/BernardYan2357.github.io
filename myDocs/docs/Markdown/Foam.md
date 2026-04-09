# Foam插件使用

Foam是一个基于VSCode的笔记工具，支持Markdown格式，可以帮助用户更好地组织和管理笔记

## 常用命令

`Ctrl + Shift + P`打开命令面板，输入以下命令：

- `Foam: Show Graph`: 显示笔记之间的关系图

## 常用格式

- `[[笔记标题]]`: Foam/Obsidian 这类工具的 wikilink 语法，MkDocs 不会自动解析
- `![[笔记标题]]`: Foam/Obsidian 的嵌入语法，MkDocs 同样不会自动解析

如果要在 MkDocs 里做页面跳转，请改用标准 Markdown 链接，例如 `[标题](../Markdown/Markdown.md)` 或 `[标题](../linux/linux.md)`