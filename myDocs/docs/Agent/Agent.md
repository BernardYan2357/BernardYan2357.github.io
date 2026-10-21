# Agent

references:

- [AI Agent(智能体) 教程](https://www.runoob.com/ai-agent/ai-agent-tutorial.html)
- [Prompt, Agent, MCP 是什么](https://www.bilibili.com/video/BV1aeLqzUE6L/)

Agent 在 AI 语境下，指的是一种能够感知环境、进行推理、做出决策并采取行动的智能系统。区别于传统的仅仅进行对话的 AI，Agent 的核心特征是自主性，它可以在无需人类监督的情况下，追求并达成复杂的任务目标

## Coding Agent

Coding Agent 是一种专门设计用于编写和维护代码的智能体，主流的有：

- [Codex](https://github.com/openai/codex)
- [Open Code](https://github.com/anomalyco/opencode)
- [Claude Code](https://code.claude.com/docs/en/overview)

### Coding plan

- ChatGPT Plus 
- 方舟 Agent Plan：用过 9.9/月的套餐，额度还可以，不过重度使用时经常会卡在5小时限额。刚开始使用的流畅度不错，后期频繁出现思考中断的问题，只有豆包模型是流畅的（不演了）。此外还会捆绑使用字节的豆包搜索和一众其它插件，感觉电脑都被污染了
- opencode go：10美元/月，支持支付宝付款。没用过，但是网上风评不好：不守诚信，砍额度；容易断连，会降速
- command go/goat：go是1美元/月，goat是10美元/月，对标 opencode go，没用过

免费 token：Nvidia API，免费，模型非常多，唯一的缺点就是特别慢，但是他都免费了还说啥了

### Codex

常用命令

```bash
# 安装 Codex CLI
npm install -g @openai/codex
# 查看 Codex CLI 版本
codex --version
# 查看 Codex CLI 帮助
codex --help
# 打开 Codex CLI
codex
# 继续上次的 Codex 会话
codex resume # 这会打开 codex 会话列表
```

#### opencodex

### OpenCode

references: [OpenCode 教程](https://www.runoob.com/opencode/opencode-tutorial.html)

OpenCode 配置文件 (opencode.json, AGENTS.md, hooks/ 等)：

- Windows: `%USERPROFILE%\.config\opencode\`
- Linux: `~/.config/opencode/`
OpenCode 缓存文件 (models.json, packages/ 等)：
- Windows: `%USERPROFILE%\.cache\opencode\`
- Linux: `~/.cache/opencode/`
OpenCode 会话数据库 (opencode.db)：
- Windows: `%APPDATA%\opencode\`
- Linux: `~/.local/share/opencode/`

可以在 WSL2 中通过符号链接的方式将 Windows 的配置文件链接到 WSL2 中（数据库不可以，跨系统了），例如：

```bash
rm -rf ~/.config/opencode ~/.cache/opencode/models.json # 删除原有的配置文件和数据库
ln -s /mnt/c/Users/ASUS/.config/opencode ~/.config # 链接配置文件
ln -s /mnt/c/Users/ASUS/.cache/opencode/models.json ~/.cache/opencode/models.json # 链接模型缓存文件
```

#### 添加 Skill

- 在项目根目录添加目录：`.opencode/skills/技能名/SKILL.md`
- 在全局路径添加目录：`~/.config/opencode/skills/技能名/SKILL.md`

也可以通过命令行添加 Skill：

```bash
npx skills add <owner>/<repo>
npx skills add <owner>/<repo> --skill <skill-name> # 安装指定仓库的特定 skill
npx skills add <owner>/<repo> -g -a claude-code # 全局安装（-g）+ 指定目标工具（-a）
```

通过这种方式安装的 Skill 会被放在全局路径下：`%USERPROFILE%\.agents\skills\技能名\`，该路径也能被 OpenCode 识别并加载

添加飞书 Skill：

```bash
npx skills npx skills add larksuite/cli --list # 查看飞书 CLI 仓库里有哪些 Skill 可用
npx skills add larksuite/cli --agent opencode
# 通过 --agent 参数指定安装到 OpenCode，也可以通过 --skill 参数指定安装特定的 Skill，不过不指定也会有列表让你选择
npm install -g @larksuite/cli # 安装飞书 CLI 工具
lark-cli config init
lark-cli auth login
lark-cli auth status
```

#### 添加 Plugin

- 在项目根目录添加目录：`.opencode/plugins/`
- 在全局路径添加目录：`%USERPROFILE%\.config\opencode\plugins\`
- 插件文件使用 `JavaScript` 或 `TypeScript` 编写，OpenCode 会在启动时自动加载
- 也可以在 `opencode.json` 里通过 `plugin` 选项加载 npm 插件或本地插件路径

例如：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-helicone-session", "@my-org/custom-plugin"]
}
```

如果想给整个 OpenCode 配置一套通用插件，放到全局目录最方便；如果只想对某个项目生效，就放到项目里的 `.opencode/plugins/`
