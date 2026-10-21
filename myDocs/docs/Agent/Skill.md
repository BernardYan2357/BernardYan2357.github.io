# Skill

## Skill 的安装和管理

### 卸载

直接删除对应的 Skill 文件夹（全局路径或项目路径）

## Skill 收藏

### Matlab

Matlab 的 skill 在调用时启动一个新的窗口，这个窗口会启用 MCP 供 Agent 调用。如果我们只想用旧窗口（旧窗口的工作区有想要被 Agent 读取的变量），可以在旧窗口命令行运行：

```m
enableservice('AutomationServer', true)
```

这样旧窗口内容也可以被 Agent 查询到

Humanizer：去ai味