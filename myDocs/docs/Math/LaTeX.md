# LaTeX

LaTeX 是一种基于 TeX 的文档准备系统，广泛用于科学、技术、工程和数学领域的文档编写。LaTeX 提供了强大的功能来处理复杂的数学公式、图表和文献引用，使得它成为学术界的标准工具之一

## 数学公式

### 语法

一般语法规则如下：

- 命令：以反斜杠 `\` 开头，如 `\alpha`、`\sum`
- 参数：用花括号 `{}` 包围，如 `\frac{a}{b}`
- 下标：使用 `_`，如 `x_1`
- 上标：使用 `^`，如 `x^2`
- 分组：用花括号 `{}` 将多个字符组合，如 `x_{i+1}`
- 行内公式：用单个美元符号 `$` 包围，如 `$E=mc^2$`
- 块级公式：用双美元符号 `$$` 包围，如
  $$
  E=mc^2
  $$
- 多行公式：使用 `\begin{align} ... \end{align}` 环境，行间用 `\\` 分隔，如：
  $$
  \begin{align}
  a+b\\
  c+d
  \end{align}
  $$

### 数学符号

#### 运算符

| 类别      | LaTeX 写法                                           | 渲染效果                                             |
| :------ | :------------------------------------------------- | :----------------------------------------------- |
| 加减乘除    | `$a+b,\ a-b,\ a\times b,\ a\div b$`                | $a+b,\ a-b,\ a\times b,\ a\div b$                |
| 点积与叉积   | `$a \cdot b,\ a \times b$`                         | $a \cdot b,\ a \times b$                         |
| 分式与根号   | `$\frac{a+b}{c},\ \sqrt{x}$`                       | $\frac{a+b}{c},\ \sqrt{x}$                       |
| 幂与指数    | `$(a+b)^x$`                                        | $(a+b)^x$                                        |
| 等式关系    | `$a\equiv b,\ b\neq c,\ c=d$`                      | $a\equiv b,\ b\neq c,\ c=d$                      |
| 大小比较    | `$a<b\le c\ge d>e$`                                | $a<b\le c\ge d>e$                                |
| 近似关系    | `$a\approx b,\ b\sim c,\ c\cong d$`                | $a\approx b,\ b\sim c,\ c\cong d$                |
| 集合关系    | `$a\in A,\ a\notin B,\ A\subset B,\ A\subseteq C$` | $a\in A,\ a\notin B,\ A\subset B,\ A\subseteq C$ |
| 集合运算与空集 | `$A\cup B,\ A\cap C,\ A=\emptyset$`                | $A\cup B,\ A\cap C,\ A=\emptyset$                |
| 取整符号    | `$\lfloor x\rfloor,\ \lceil x\rceil$`              | $\lfloor x\rfloor,\ \lceil x\rceil$              |
| 取反符号    | `$\bar{x}$`                                        | $\bar{x}$                                        |

#### 特殊函数与符号

| 类型   | LaTeX 写法                   | 渲染效果                      |
| :--- | :------------------------- | :------------------------ |
| 三角函数 | `$\sin,\ \cos,\ \tan$`     | $\sin,\ \cos,\ \tan$      |
| 对数   | `$\log,\ \ln$`             | $\log,\ \ln$              |
| 极限   | `$\lim_{x \to 0}$`         | $\lim_{x \to 0}$          |
| 求和   | `$\sum_{i=1}^{n}$`         | $\sum_{i=1}^{n}$          |
| 积分   | `$\int_{a}^{b}$`           | $\int_{a}^{b}$            |
| 无穷   | `$\infty$`                 | $\infty$                  |
| 向量   | `$\vec{v}$`                | $\vec{v}$                 |
| 省略号  | `$\cdots,\ \ldots$ \vdots` | $\cdots, \ldots , \vdots$ |

#### 矩阵表示

| 类型    | 环境        | LaTeX 写法                                         | 渲染效果                                           |
| :---- | :-------- | :----------------------------------------------- | :--------------------------------------------- |
| 圆括号矩阵 | `pmatrix` | `$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$` | $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ |
| 方括号矩阵 | `bmatrix` | `$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$` | $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ |
| 花括号矩阵 | `Bmatrix` | `$\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}$` | $\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}$ |
| 行列式   | `vmatrix` | `$\begin{vmatrix} a & b \\ c & d \end{vmatrix}$` | $\begin{vmatrix} a & b \\ c & d \end{vmatrix}$ |

### 希腊字母

[希腊字母](https://xilazimu.net/)

| 小写 LaTeX命令 | 小写字母 | 大写 LaTeX命令 | 大写字母 |
| :-----: | :-----: | :-----: | :----: |
| `\alpha` | α | - | Α |
| `\beta` | β | - | Β |
| `\gamma` | γ | `\Gamma` | Γ |
| `\delta` | δ | `\Delta` | Δ |
| `\epsilon` | ε | - | Ε |
| `\zeta` | ζ | - | Ζ |
| `\eta` | η | - | Η |
| `\theta` | θ | `\Theta` | Θ |
| `\iota` | ι | - | Ι |
| `\kappa` | κ | - | Κ |
| `\lambda` | λ | `\Lambda` | Λ |
| `\mu` | μ | - | Μ |
| `\nu` | ν | - | Ν |
| `\xi` | ξ | `\Xi` | Ξ |
| `\omicron` | ο | - | Ο |
| `\pi` | π | `\Pi` | Π |
| `\rho` | ρ | - | Ρ |
| `\sigma` | σ | `\Sigma` | Σ |
| `\tau` | τ | - | Τ |
| `\upsilon` | υ | `\Upsilon` | Υ |
| `\phi` | φ | `\Phi` | Φ |
| `\chi` | χ | - | Χ |
| `\psi` | ψ | `\Psi` | Ψ |
| `\omega` | ω | `\Omega` | Ω |

注：部分大写希腊字母在 LaTeX 中没有单独命令，通常直接使用对应的字母外形显示
