# Markdown

references:
- [Markdown 教程](https://markdown.com.cn/)

## 语法

### 复选框

```markdown
- [ ] 未完成的任务
- [x] 已完成的任务
- [ ] 另一个待办
```

呈现出的效果：

- [ ] 未完成的任务
- [x] 已完成的任务

## 语法变通

由于 Markdown 语法兼容 HTML，所以可以在 Markdown 中使用 HTML 标签来实现一些 Markdown 不支持的语法。HTML 语法参考：[[Web/HTML]]

### 下划线

Markdown语法不支持下划线，但可以使用`<ins>`标签来实现下划线效果，例如：

<ins>This text will be underlined.</ins>

### 缩进

Markdown 里的空格和制表符有特殊用途，比如创建换行或代码块。如果你想用 Tab 缩进段落，可以使用 HTML 的 `&nbsp;` 实体来创建空格，例如：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This paragraph is indented with 8 spaces.

### 图片

Markdown 原生不支持设置图片尺寸和对齐方式，此时可以使用 HTML 的 `<img>` 标签：

```html
<img src="https://example.com/image.png" alt="替代文字" width="300" align="center" />
```

- `width`：控制图片宽度（也可用 `height` 控制高度）
- `align`：控制对齐方式，取值 `left`、`center`、`right`

也可以使用 `scale` 属性：



#### 图片标题（Caption）

需要为图片添加说明文字时，可以用 `<figure>` 与 `<figcaption>` 标签组合：

```html
<figure>
  <img src="https://example.com/image.png" alt="替代文字" width="400" />
  <figcaption>这是图片的说明文字</figcaption>
</figure>
```

#### 点击图片跳转

将图片嵌套在链接中，即可实现点击图片跳转到目标地址：

```markdown
[![替代文字](图片地址)](目标链接地址)
```

## 扩展

Markdown 的扩展语法可以通过一些第三方库来实现

### LaTeX

Markdown 标准语法本身没有 LaTeX 数学公式语法，但许多 Markdown 编辑器和渲染器支持通过扩展来使用 LaTeX 语法来编写数学公式，LaTex 语法参考：[[Math/LaTeX]]