# md数学公式

在 Markdown 中，数学公式通过 LaTeX 语法来表示。

## 基本语法结构

- 命令：以反斜杠 \ 开头，如 `\alpha`、`\sum`
- 参数：用花括号 {} 包围，如 `\frac{a}{b}`
- 下标：使用 _，如 `x_1`
- 上标：使用 ^，如 `x^2`
- 分组：用花括号将多个字符组合，如 `x_{i+1}`

## 行内公式与块级公式

- 行内公式：用单个美元符号 `$` 包围，如 $E=mc^2$
- 块级公式：用双美元符号 `$$` 包围，如

$$
E=mc^2
$$

- 多行公式：使用 `\begin{align} ... \end{align}` 环境，如

$$
\begin{align}
a+b\\
c+d
\end{align}
$$

## Latex命令

### 希腊字母

| LaTeX命令   | 希腊字母  | LaTeX命令   | 希腊字母  |
|:-----------:|:--------:|:-----------:|:--------:|
| `\alpha`    | α        | `\nu`       | ν        |
| `\beta`     | β        | `o`         | ο        |
| `\gamma`    | γ        | `\pi`       | π        |
| `\delta`    | δ        | `\rho`      | ρ        |
| `\epsilon`  | ε        | `\sigma`    | σ        |
| `\theta`    | θ        | `\tau`      | τ        |
| `\lambda`   | λ        | `\phi`      | φ        |
| `\mu`       | μ        | `\omega`    | ω        |

### 数学符号

#### 运算符

$$
\begin{align}
a+b\\
a-b\\
a\times{b}\\
a\div{b}\\
\frac{a+b}{c}\\
\sqrt{x}\\
(a+b)^{x}\\
a\equiv{b}\neq{c}={d}\\
a<b\leq{c}\geq{d}>e\\
a\approx{b}\sim{c}\cong{d}\\
a\in{A},a\notin{B}\\
A\subset{B},A\subseteq{C}\\
A\cup{B},A\cap{C}\\
A=\emptyset{}\\
\end{align}
$$

#### 特殊函数与符号

- 三角函数：$\sin, \cos, \tan$
- 对数：$\log, \ln$
- 极限：$\lim_{x \to 0}$
- 求和：$\sum_{i=1}^{n}$
- 积分：$\int_{a}^{b}$
- 无穷：$\infty$

#### 矩阵表示

圆括号：`pmatrix`

$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

方括号：`bmatrix`

$$
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
$$

花括号：`Bmatrix`

$$
\begin{Bmatrix}
a & b \\
c & d
\end{Bmatrix}
$$

行列式：`vmatrix`

$$
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
$$

