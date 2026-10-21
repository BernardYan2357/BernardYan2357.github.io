# FreeCAD

references：

- [FreeCAD Documentation](https://wiki.freecad.org/Main_Page)
- [FreeCAD Tutorial for beginners（视频）](https://www.bilibili.com/video/BV18dAsepEyx)

FreeCAD 是一款开源的**参数化 3D CAD** 软件

## 参数化 3D CAD

参数化 3D CAD 的最大特点就是模型文件不只存储当前的几何形状，还存储了模型的设计历史和参数关系

- 设计历史：模型文件记录了从最初的草图到最终的三维模型的每一步的操作，使得用户可以回溯和修改设计历史中的任何一步
  ![[设计历史.png]]
- 参数关系：模型文件还存储了各个设计元素之间的参数关系，例如我们在草图中添加的多种约束以及定义的参数。这些参数关系使得用户可以通过修改参数来自动更新整个模型，而不需要手动调整每个相关的设计元素

## 快捷键

选择 Blender 风格的快捷键

## 绘制螺纹

若要绘制一些带螺纹紧固件，可以使用 [Fasteners Workbench](https://wiki.freecad.org/Fasteners_Workbench)得到一些预制的紧固件模型

[使用 FreeCAD 绘制螺纹 | 前尘逐梦](https://qianchenzhumeng.github.io/posts/make_threaded_part_in_freecad/)和[Thread_for_Screw_Tutorial | FreeCAD Docs](https://wiki.freecad.org/Thread_for_Screw_Tutorial) 介绍的方法大致相同，都是绘制螺纹线，再绘制螺纹的垂直剖面，通过`PartDesign AdditivePipe`填充出螺纹。这种方法过于繁杂，不过具备普遍性，可以参考。此外，前尘逐梦的对于螺纹末端的处理方法可以改进为使用`PartDesign SubtractiveBox（减料图元）`来减除末端多余的螺纹

 [Freecad 建模设计 带孔螺栓螺帽套件 保姆级教程](https://www.youtube.com/watch?v=xkGxSy7ZOZk)中介绍的方法则更加方便，利用FreeCAD更新的`PartDesign Hole`选项，选择任意的螺纹标准，由软件自动绘制螺纹。再绘制一个无孔的原物体，通过`Part Cut` 选项进行剪切，得到外凸的螺纹

## 模型转换

### mesh 转换为 solid

mesh(网格)是由许多小的三角形组成的表面模型，shape(形状)是网格经过处理后得到的三维模型，而 body(实体)是一个完整的三维对象，具有体积和质量属性

转换步骤：

1. 导入 mesh：STL 文件格式是常见的 mesh 格式
2. 选中网格模型，切换到 Part 工作台，在零件一栏选中`从网格生成形状`，将模型从 mesh 转换为 shape
   - 跳出的对话框中，可以选择`是否缝合形状`。选择缝合形状可以把网格模型里不连续的的面片/顶点缝合起来，形成一个封闭的、水密的实体。缝合形状的容差决定了 FreeCAD 会把多近的顶点/面片当成同一个点来缝合，数值越小缝合越挑剔，生成的模型更接近原始 STL 的细节，但对模型质量要求高，有小破洞可能缝不上，导致生成失败；数值越大缝合越宽松，会丢失一些精细细节，甚至把原本分开的特征合并在一起。不勾选的话，可能会生成有缝隙、破面的曲面，后续操作会报错
1. 再次在零件一栏选中`从形状生成实体`，将 shape 转换为 body

## Add Addon 

在 FreeCAD 中可以通过 **工具->Addon Manager** 来安装和管理由社区提供的外部工作台（External Workbench）、宏（Marcos）和首选项包（Preference Pack）

一些有用的外部工作台插件：

- [Fasteners Workbench](https://wiki.freecad.org/Fasteners_Workbench)：add various fasteners（紧固件） to parts、
- [RobotCAD](https://github.com/drfenixion/freecad.robotcad)：将模型导出为 URDF/Xacro

## 问题记录

### Wire is not closed when Pading or Pocketing

若确认草图无非闭合图形时仍报错，将外部投影的点线设置为辅助线