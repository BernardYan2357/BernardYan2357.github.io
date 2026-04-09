# opencv

## 安装

### windows

点击链接[下载](https://opencv.org/releases/)，选择 Windows 平台，将 OpenCV 解压

#### VisualStudio

打开Visual Studio，创建一个新的C++项目，右键点击项目，选择属性：
1. 修改“附加包含目录”（定位头文件）
  - 进入 C/C++ -> 常规 -> 附加包含目录，将路径修改为`~\OpenCV\build\includes`
2. 配置“附加库目录”（定位库文件）
  - 进入左侧的 链接器 (Linker) -> 常规 (General) -> 附加库目录，填写`~\OpenCV\build\x64\vc16\lib`
3. 配置“附加依赖项”（指定具体的 lib 文件）
  - 进入 链接器 (Linker) -> 输入 (Input) -> 附加依赖项，添加`D:\Program Files\OpenCV\build\x64\vc16\lib`目录下的lib文件名，根据项目配置（Debug 或 Release）选择正确的 lib 文件：
    - 如果当前是 Debug 配置，填入：opencv_world4130d.lib（以 d 结尾，4130 代表 OpenCV 4.13.0，根据实际版本号修改）
    - 如果是 Release 配置，填入：opencv_world4130.lib（不带 d）
4. 配置环境变量（运行时找到 DLL 文件）
  - 将 OpenCV 的 `build\x64\vc16\bin` 目录添加到系统环境变量 PATH 中，这样在运行时程序才能找到 OpenCV 的 DLL 文件

#### MSVC+CMake+VSCode

1. 新建一个系统或者用户环境变量，命名为 `OpenCV_DIR`，值为 OpenCV 的 lib 目录路径：`~\OpenCV\build\x64\vc16\lib`
2. 打开 VSCode，安装 CMake Tools 插件
3. 创建一个文件夹作为项目目录，在该目录下创建 `CMakeLists.txt` 文件，内容如下：
  ```cmake
  cmake_minimum_required(VERSION 3.20) # 指定 CMake 的最低版本要求
  project(learn_opencv LANGUAGES CXX) # 定义项目名称为 learn_opencv，并指定使用 C++ 语言

  set(CMAKE_CXX_STANDARD 17) # 设置 C++ 标准为 C++17
  set(CMAKE_CXX_STANDARD_REQUIRED ON) # 确保使用指定的 C++ 标准，如果编译器不支持则会报错

  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /utf-8") # 将编译器的字符集设置为 UTF-8，确保源代码中的非 ASCII 字符能够正确处理

  find_package(OpenCV REQUIRED) # 查找 OpenCV 库，如果没有找到则会报错

  add_executable(bonocularCamera bonocularCamera.cpp) # 定义一个可执行文件，名称为 binocularCamera，源文件为 binocularCamera.cpp
  target_link_libraries(bonocularCamera PRIVATE ${OpenCV_LIBS}) # 将 OpenCV 库链接到 binocularCamera 可执行文件，PRIVATE 表示链接仅对该 目标可见

  # 可选：输出 OpenCV 的相关信息，方便调试和确认配置是否正确
  message(STATUS "OpenCV version: ${OpenCV_VERSION}") # 输出 OpenCV 的版本信息到 CMake 的状态消息中
  message(STATUS "OpenCV include: ${OpenCV_INCLUDE_DIRS}") # 输出 OpenCV 的包含目录信息到 CMake 的状态消息中
  ```
4. 在 VSCode 中打开命令面板（Ctrl+Shift+P），选择 CMake: Configure，选择生成器`Visual Studio Community 2022 Release - amd64`
5. 命令行执行：
  ```bash
  cmake -B build -S . # 生成构建文件，-B 指定构建目录，-S 指定源代码目录
  cmake -B build -S . -DCMAKE_BUILD_TYPE=Release # 指定构建类型为 Release

  cmake --build build # 构建项目，-B 指定构建目录
  cmake --build build --config Release # 指定构建配置为 Release
  ```
  - 第一条命令会配置工程，生成构建系统，在未改动 CMakeLists.txt 的情况下，之后只需要执行第二条命令即可重新构建项目
  - 第二条命令会根据生成的构建系统来编译项目，生成可执行文件

> 也可以尝试将MSVC换为Ninja，[暂未尝试]

配置VSCode的C++插件，使其识别OpenCV的头文件和库文件，从而提供代码补全和错误检查功能：[[软件使用笔记/VSCode使用笔记.md#C++配置]]
