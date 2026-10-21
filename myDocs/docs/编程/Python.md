# Python

## pip

pip 是 Python 的包管理工具

### pip 换源

要使用镜像源，可以在安装包时指定`-i`参数，例如：

```bash
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

设置全局镜像源：`pip config --editor nano edit`

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 虚拟环境

虚拟环境是 Python 用来**隔离项目依赖**的机制，每个环境拥有独立的 Python 解释器和第三方包，可以避免不同项目之间的版本冲突。常用工具包括自带的 `venv`、第三方库 `virtualenv`，以及集成了包管理的 `uv`、`conda` 等

### venv

venv 是 Python 自带的轻量级虚拟环境管理模块，无需额外安装

#### 常用命令

```bash
# 创建虚拟环境
python -m venv <环境名> # 例如：python -m venv .venv
C:\Python311\python -m venv .venv # 使用指定版本的 Python 创建虚拟环境（不建议在全局中安装多个 python 版本，建议使用uv/pyenv）
# 激活虚拟环境
.\<环境名>\Scripts\activate
# 退出虚拟环境
deactivate
# 导出当前环境的包列表到 requirements.txt
pip freeze > requirements.txt
# 在新环境中根据 requirements.txt 安装依赖
pip install -r requirements.txt
```

### [uv](https://uv.doczh.com/)

uv 是一个现代化的 Python 包管理工具，提供了从安装 Python 到创建虚拟环境、管理依赖、安装包等功能，速度比传统 pip 快 10-100 倍

#### 常用命令

```bash
# 创建虚拟环境
uv venv                      # 默认在当前目录创建 .venv 文件夹
uv venv --python 3.11        # 指定 Python 版本
uv venv myenv                # 指定环境名
# 激活/退出虚拟环境：与venv相同
# 安装包
uv pip install requests
	-i https://pypi.tuna.tsinghua.edu.cn/simple # 指定国内源
uv pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128 # 安装指定版本的包
uv pip install -r requirements.txt # 从 requirements.txt 安装
# 管理依赖
uv add requests # 添加包并写入 pyproject.toml
uv sync # 根据 pyproject.toml 同步环境
uv pip freeze > requirements.txt # 导出当前环境包列表
# 运行脚本
uv run script.py
```

- `uv venv` 创建的环境与 `python -m venv` 完全兼容，可以混用
- 如果系统没有安装指定 Python 版本（如 `uv venv --python 3.12`），uv 会自动从官网下载，无需手动安装
- `uv` 同样支持 pip 的配置文件（如 `pip.conf`），无需额外配置
- `pyproject.toml` 是 Python 项目的配置文件，用于集中管理项目元数据、构建系统配置、依赖声明等，旨在逐步替代传统的 `setup.py`、`requirements.txt`、`setup.cfg` 等分散文件

## Python 语法

### 类型

在 Python 中，变量声明时应使用`: `来进行类型注解：

```python
bool flag = false # 错误！
flag: bool = false
```

`->`符号在 Python 中用于函数注解，表示函数的返回类型。例如：

```python
def add(a: int, b: int) -> int:
    return a + b
```

### 类

Python 的类没有私有成员的说法，要想声明这是一个私有成员，在变量名或函数名之前加下划线，例如：`_private_var`，注意这只是一个约定

### Lambda

Lambda 表达式用于创建**匿名函数**，语法为：

```python
lambda 参数列表: 表达式
```

它等价于一个没有名字的函数，`:` 后面只能是**单个表达式**，该表达式的值会被自动返回（不能写 `return`，也不能包含语句）

```python
# 普通函数
def add(a, b):
    return a + b

# 等价的 lambda
add = lambda a, b: a + b
add(1, 2)  # 3
```

lambda 支持默认参数、可变参数等各种参数形式：

```python
lambda x: x * x            # 一个参数
lambda x, y=10: x + y      # 默认参数
lambda *args: sum(args)    # 可变位置参数
lambda **kwargs: kwargs    # 可变关键字参数
```

lambda 最常见的用途是作为 `sorted`、`map`、`filter` 等函数的 key 或回调：

```python
nums = [3, 1, 2]
sorted(nums, key=lambda x: -x)          # [3, 2, 1]，按降序

pairs = [(1, "b"), (2, "a")]
sorted(pairs, key=lambda p: p[1])       # 按元组第二个元素排序

list(map(lambda x: x * 2, nums))        # [6, 2, 4]
list(filter(lambda x: x > 1, nums))     # [3, 2]
```

逻辑复杂（多行、需要语句或类型注解）时应使用普通的 `def`，不要硬塞进 lambda

### with

`with` 是 Python 的**上下文管理器**语法，用来在进入和退出某个“上下文”时自动做一些设置和清理。可以看作是一个作用域的声明

```python
with tf.variable_scope("base"):
    w = tf.get_variable("weight", shape=[3, 3, 64, 128])
# 变量 W 的完整名字通常会变成：base/weight
```

### 装饰器

在Python中，装饰器是一种以特定格式编写的函数，用于修改其他函数的行为。装饰器用于在函数定义之前应用修改，可以在不修改原函数代码的情况下添加额外的功能。

使用 `@` 符号可以将装饰器应用于函数。例如，下面是一个简单的装饰器示例，用于在函数执行前后打印日志信息：

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print("函数开始执行")
        result = func(*args, **kwargs)
        print("函数执行结束")
        return result
    return wrapper

@log_decorator
def my_function():
    print("这是一个函数")
```

装饰器被广泛用于第三方库中，例如 FastMCP 中的`@mcp.tool()`装饰器，用于将函数注册为工具，使其能够被 Agent 调用

## Python 常用库

### time

`time` 是 Python 标准库，提供时间获取、格式化和程序暂停等功能

#### 获取时间戳

```python
import time

time.time()      # 1726400000.123，从 1970-01-01 00:00:00 UTC 至今的秒数（float）
time.time_ns()   # 纳秒级时间戳（int）
```

#### 程序暂停

```python
time.sleep(2)    # 暂停 2 秒，参数可以是浮点数，如 0.5
```

#### 计时

```python
start = time.perf_counter()
# ... 要测量的代码 ...
end = time.perf_counter()
print(f"耗时 {end - start:.4f} 秒")
```

- `perf_counter()` 精度最高，包含 sleep 时间，适合测量代码运行耗时
- `monotonic()` 是单调时钟，保证不会因系统时间被修改而回退，适合计算超时

#### 结构化时间 struct_time

```python
t = time.localtime()   # 本地时间
t.tm_year              # 年，如 2026
t.tm_mon               # 月
t.tm_mday              # 日
t.tm_hour              # 时

time.gmtime()          # UTC 时间
```

#### 格式化与解析

```python
# struct_time -> 字符串
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # '2026-09-16 10:30:00'

# 字符串 -> struct_time
time.strptime("2026-09-16", "%Y-%m-%d")

# 快速得到可读字符串
time.ctime()          # 'Wed Sep 16 10:30:00 2026'
```

常用格式符：`%Y` 四位年、`%m` 月、`%d` 日、`%H` 24 小时制时、`%M` 分、`%S` 秒

#### 时间戳与 struct_time 互转

```python
time.mktime(time.localtime())  # struct_time -> 时间戳
time.localtime(time.time())    # 时间戳 -> struct_time
```

> 涉及日期加减、时区等复杂运算时，建议使用 `datetime` 标准库；`time` 更适合计时、暂停和简单格式化

### numpy

