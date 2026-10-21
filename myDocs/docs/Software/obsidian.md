# obsidian

## 忽略目录下的特定子文件夹

在 Obsidian 中，可以通过 **文件与链接 -> 高级 -> 忽略文件** 忽略部分子文件夹或文件，常用 glob 规则如下：

- `Projects/node_modules` – 忽略 `Projects` 下的 `node_modules`
- `**/node_modules` – 忽略所有位置的 `node_modules`
- `**/dist/*` – 忽略所有 `dist` 文件夹内的内容

保存后，这些内容不会出现在文件列表、搜索、快速切换和关系图谱中

该方法可以用来忽略 copilot 插件产生的 .md 文件