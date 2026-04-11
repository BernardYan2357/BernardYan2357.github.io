# VSCode快捷键

- 代码建议：`Ctrl + Space`

- 延伸光标至多行：`鼠标中键`
- 撤销：`Ctrl + Z` 恢复：`Ctrl + Y`
- 保存：`Ctrl + S`
- 编译：`Ctrl + Shift + B`
- 快速选中单词
  - 在单词所在处置光标，双击左键选中
  - 键盘操作：`Ctrl + D`，再次按下会继续选中下一个相同的单词，`Ctrl + Shift + L` 可以选中所有相同的单词

markdown 快捷键：

- 粗体：`Ctrl + B`
- 斜体：`Ctrl + I`

# VSCode配置

VSCode可以使用json文件进行配置，位于`.vscode`文件夹中的`settings.json`文件中。也可以通过图形界面进行配置，打开图形界面在右上角可以切换为json视图

## IntelliSense配置

- [VSCode IntelliSense 完全配置指南（C++/Python/JavaScript）](https://www.cnblogs.com/ljbguanli/p/19224402)

配置 IntelliSense 的本质就是建立三个关键连接：

- 第一个连接是让 VS Code 知道"你用什么工具写代码"。比如 Python 项目需要指定 Python 解释器，C++ 项目需要指定编译器
- 第二个连接是让 VS Code 知道"你的依赖库在哪里"。你安装的第三方库、自定义的工具模块，这些资源的位置需要明确告知编辑器
- 第三个连接是让 VS Code 理解"你的项目结构"。哪些文件需要分析，哪些文件夹可以忽略，代码之间的引用关系是怎样的

### C++配置

C/C++ 的配置核心是让编辑器找到头文件。当你写`#include <stdio.h>`或`#include "myheader.h"`时，编译器需要知道这些头文件在哪里，VSCode 也需要知道，才能提供正确的函数签名提示

1. 安装插件：C/C++
2. 按`Ctrl+Shift+P`打开命令面板，输入"C/C++: Edit Configurations (JSON)"，会在`.vscode`文件夹下生成`c_cpp_properties.json`文件
3. 在`c_cpp_properties.json`文件中，找到`includePath`字段，添加头文件路径：
   ```json
   "includePath": [
       "${workspaceFolder}/**", // ${workspaceFolder} 是路径变量，它代表"当前打开的项目根目录"
       "D:\\Program Files\\OpenCV\\build\\includes", // 这是 OpenCV 的头文件路径，根据实际安装位置修改
       "/home/bernard/arm_ws/install/robot_arm_interfaces/include/**" // 这是 ROS2 的头文件路径，根据实际安装位置修改
   ],
   ```

## 解释器配置

### python配置

安装插件：PythonEnvironment

- 使用命令面板配置解释器
   - 按下 `Ctrl + Shift + P` 打开命令面板，输入 `Python: Select Interpreter` 并选择，选择合适的 Python 解释器
- 使用状态栏配置解释器（打开python文件时出现）
   - 点击状态栏左下角的 Python 版本号，选择合适的 Python 解释器
- 创建`settings.json`文件（为特定文件夹永久设置解释器）
    - 在工作区根目录下创建 `.vscode` 文件夹，在 `.vscode` 文件夹中创建 `settings.json` 文件，添加以下内容：
```json
{
   "python.pythonPath": "path/to/your/python" // 替换为实际的 Python 解释器路径
}
```
- 查看当前 Python 解释器
   - 在命令面板中输入 `Python: Show Output`，可以查看当前使用的 Python 解释器路径

# VSCode美化

毛玻璃效果：安装插件`Vibrancy Continued`

主题插件：

- Catppuccin for VSCode
- Catppuccin Icons for VSCode
- SynthWave'84：提供霓虹灯风格字体
- Vim Theme：提供经典Vim主题
- Nebula Theme
- Halcyon Theme
- Blueberry dark Theme