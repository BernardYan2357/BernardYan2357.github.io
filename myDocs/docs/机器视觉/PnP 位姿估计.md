# PnP 位姿估计

单目相机成像时，图像中只能直接得到特征物体的像素坐标，缺少深度信息。一般提到三维空间点位姿计算，通常容易想到深度相机；但实际上，只要已知特征物体自身的几何结构，单目相机同样可以恢复出三维位姿

这里的前提条件是：
- 已知至少三个特征点在物体坐标系下的三维坐标，以及它们在图像中的像素坐标。一般使用标定板（棋盘格等）或[[AprilTag&ArUco]]来得到准确的三维坐标
- 已知相机的内参和畸变参数，可以通过[[相机标定]]得到

然后即可使用 PnP（Perspective-n-Point）算法求解空间位姿。PnP 位姿估计的代码可以通过 OpenCV 库函数实现：[PnP位姿估计.ipynb at opencv · BernardYan2357/my_notebook](https://github.com/BernardYan2357/my_notebook/blob/opencv/PnP%E4%BD%8D%E5%A7%BF%E4%BC%B0%E8%AE%A1.ipynb)

核心函数是：

```python
ok, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
```

## Camera 2 Base 的标定

TODO 应该被优化到手眼标定里

通过 OpenCV 库函数 `cv2.solvePnP()` 得到的是标记坐标系坐标到相机坐标系的变换 $T^C_M$。在实际应用中，我们需要的通常是标记相对于某个固定坐标系的位姿（例如机械臂的基座坐标系），从而方便我们对物体的操作

$$ T^B_M = T^B_C \cdot T^C_M $$

其中 B 表示基座坐标系（Base），M 表示标记坐标系（Marker），C 表示相机坐标系（Camera）

为了得到 $T^B_M$，需要已知 $T^B_C$。$T^C_M$ 可由 `solvePnP` 实时求得，因此标定时只需将 Aruco 标记固定放置在已知位置，测量出 $T^B_M$，即可反解 $T^B_C$：

$$ T^B_C = T^B_M \cdot (T^C_M)^{-1} $$

需要明确 M、B、C 这几个坐标系的轴向约定：

- 对于 Aruco 标记，`cv2.aruco.detectMarkers()` 返回的 `corners`（像素坐标）顺序固定：左上、右上、右下、左下（顺时针）。为匹配像素与空间点，传入 `cv2.solvePnP()` 的 `objectPoints` 也必须按相同顺序排列。数组中各点的正负号则决定了标记坐标系的朝向：
```python
# 以 Aruco 中心点为原点：x 轴朝右，y 轴朝上，z 轴垂直标记平面朝外
[[-half_size,  half_size, 0.0],  # 左上
 [ half_size,  half_size, 0.0],  # 右上
 [ half_size, -half_size, 0.0],  # 右下
 [-half_size, -half_size, 0.0]]  # 左下
```
- 对于基座坐标系，其轴向约定应与 URDF 中定义的一致
- 对于相机，其遵循 OpenCV 的光学坐标系惯例（Z 轴指向视线方向、X 轴向右、Y 轴向下），注意这与其安装位姿无关