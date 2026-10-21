# ROS2 可视化

## rqt_image_view

在 ROS2 中，可视化图像最常用的工具是：`rqt_image_view`，一个基于 Qt 的图像显示插件，支持订阅任意 `sensor_msgs/msg/Image` 话题并实时显示图像
- 安装：`sudo apt install ros-${ROS_DISTRO}-rqt-image-view`  
- 启动：`rqt_image_view` 或在 `rqt` 中选择 Plugins → Visualization → Image View

## RVIZ2

通用 3D 可视化工具，也可以添加“Image”显示类型来查看相机图像，适合与其他传感器数据（点云、TF 等）共同展示
- 启动：
	- 在 rviz2 窗口左下角，点击 **Add** 按钮
	- 在弹出的对话框中选择 **By display type** 标签页
	- 找到 **Image**，选中后点击 **OK**

### 问题记录

在 WSL2 里面带配置文件启动 rviz2 时界面无法交互，但UI中时间戳仍正常刷新

- **检查渲染负载**：时间戳继续刷新，说明 rviz 还在运行。发现环境变量 `LIBGL_ALWAYS_SOFTWARE=1` 强制使用 CPU 软件渲染，RViz CPU 占用约 650%。切换 GPU 后降到约 20%，但点击仍失效
- **检查窗口焦点和基础鼠标输入**：打开简单的 X11 测试窗口，能点击 OK，说明 WSLg 的基础鼠标输入可用
- **用默认 RViz 做对比**：启动只有网格、不加载 MoveIt 的 RViz，能正常操作。问题范围缩小到配置中的插件或布局
- **重置保存的布局**：临时移除 `Window Geometry` 中的 `QMainWindow State`，保留 MotionPlanning 插件。菜单恢复响应，说明问题与恢复旧停靠布局有关
- **重建布局并验证**：重新安排布局尺寸，用完整模拟 bringup 加载模型后，交互恢复正常

目前证据定位到了“恢复旧布局会触发异常”，还没有确定 Qt 或 WSLg 内部的具体缺陷

## cv_bridge

 使用 `cv_bridge` 将 ROS2 图像转为 OpenCV Mat，再用 `cv::imshow` 显示，适合需要对原始图像进行后处理的情景