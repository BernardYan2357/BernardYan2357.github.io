# AprilTag&ArUco

## Aruco

ArUco 标记是由宽黑色边框和确定其标识符（id）的内部二进制矩阵组成的正方形标记。它的主要优点是检测简单、快速，并且具有很强的鲁棒性

Aruco 有以下三个属性：

- Dictionary（词典）: 定义了一组预定义的Aruco标记集合，不同的词典包含不同数量和类型的标记，每个词典中所有的Aruco标记均包含相同数量的块或位
- 一个 $N \times N$ 的 Aruco 标记包含 $N \times N$ 个黑白块（除去一圈黑色边框），常见的有 4x4、5x5、6x6、7x7 等
- Marker ID（标识符ID）:  每个 Aruco 标记都有一个唯一的整数 ID，用于区分不同的标记，不同的 id 有不同的黑白块排列
- Marker size, mm（标记尺寸，毫米）： 定义了 Aruco 标记的物理尺寸

Aruco 的识别可用 OpenCV 库函数实现，详见：[Aruco标记检测.ipynb at opencv · BernardYan2357/my_notebook](https://github.com/BernardYan2357/my_notebook/blob/opencv/Aruco%E6%A0%87%E8%AE%B0%E6%A3%80%E6%B5%8B.ipynb)
