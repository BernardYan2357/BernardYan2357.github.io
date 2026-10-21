---
marp: true
theme: gaia
paginate: true
size: 16:9
header: Marp 使用指南
footer: Markdown Slides
---

# 如何使用 Marp

用 Markdown 高效制作 PPT

作者：Bernard
日期：2026-03-15

---

## 目录
- [Marp 是什么](#marp是什么)
- [安装与准备](#安装与准备)
- [幻灯片分隔规则](#幻灯片分隔规则)
- [页面级指令](#页面级指令)
- [主题与全局样式](#主题与全局样式)
- [导出方式](#导出方式)

---

## Marp是什么

- Marp = Markdown Presentation Ecosystem
- 用 Markdown 语法直接写 PPT
- 支持在 VS Code 中实时预览
- 可导出 HTML、PDF、PPTX

---

## 安装与准备

- 在 VS Code 安装扩展：Marp for VS Code
- 新建 `.md` 文件
- 在文件头加入 Marp front matter

```yaml
---
marp: true
theme: default
paginate: true
---
```

---

## 幻灯片分隔规则

使用三条横线分隔每一页：

```markdown
# 第 1 页
内容...

---

# 第 2 页
内容...
```

---

## 页面级指令

可在某一页前使用 HTML 注释设置局部样式：

```markdown
<!--
_class: lead
_paginate: false
-->
```

常见用途：
- 封面页隐藏页码
- 单页切换强调样式

---

## 主题与全局样式

可选主题：
- `default`
- `gaia`
- `uncover`

如需更深度定制，可配合 CSS 文件。

---

## 导出方式

在 VS Code 中：

- `Ctrl + Shift + P`
- 输入 `Marp: Export Slide Deck...`
- 选择导出格式（HTML/PDF/PPTX）
