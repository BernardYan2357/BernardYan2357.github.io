# MCP

MCP 是 Anthropic 推出的一套开放的标准化协议，核心逻辑是：将各工具程序的接口进行统一规范化，使得 Agent 可以通过标准化的接口调用不同的工具程序，而不需要关心工具程序的具体实现细节

## MCP by Python

references:

- [Python MCP](https://pypi.org/project/mcp/#what-is-mcp)

编写MCP，本质上就是编写给AI Agent调用的函数，MCP Server 不像是服务器，更像是一个脚本

### Write MCP Server

假设我们要编写一个获取主机信息的MCP Server，首先需要编写一个工具函数来获取主机信息，例如：

```python
# tools.py
import platform
import psutil
import json

def get_host_info() -> str:
    """get host information
    Returns:
        str: the host information in JSON string
    """
    info: dict[str, str] = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": str(round(psutil.virtual_memory().total / (1024**3), 2)),
    }
    return json.dumps(info)
```

工具函数的编写需要注意以下几点：

- 工具函数的输入参数最好为字符串类型
- 工具函数需要返回字符串类型的数据
- 工具函数需要处理好异常情况，避免抛出未捕获的异常，可以通过返回错误信息的字符串来告知Agent发生了错误
- 工具函数名称需要具有描述性，必要时使用"""docstring"""来说明函数的功能和输入输出

然后我们需要编写MCP Server来注册这个工具函数，例如：

```python
# main.py
from mcp.server.fastmcp import FastMCP
import tools
mcp = FastMCP("host info mcp") # MCP名称，可以随意取，建议具有描述性
mcp.add_tool(tools.get_host_info)
@mcp.tool()
def foo():
    return ""
def main():
    mcp.run("stdio")
if __name__ == "__main__":
    main()
```

工具函数的注册有两种方法：

- 使用装饰器`@mcp.tool()`，将函数注册为工具
- 直接调用`mcp.add_tool()`方法，将函数注册为工具，这种方法更适用于工具函数跨文件使用的情况

MCP Server和Agent之间的通信有三种机制：

- stdio：简单的标准输入输出通信机制，适用于server和agent在同一台机器上的情况
- sse: 基于HTTP协议的单向通信机制，适用于server和agent不在同一台机器上的情况
- streamable-http: 基于HTTP协议的双向通信机制，适用于server和agent不在同一台机器上的情况

通过`mcp.run()`方法启动MCP Server，传入通信方式，例如：

```python
mcp.run("stdio") # 参数可以是"stdio"、"sse"、"streamable-http"，分别对应三种通信机制
```
