# Face-Swapping-and-Stylizing
北京大学2020学年春季学期《算法设计与分析》课程大作业

作者：吴臻，曾子雨，周慕歆

指导老师：施柏鑫

助教：崔轩宁

---

本项目实现了基于对抗生成网络（GAN）和泊松编辑(Possion Image Editing)的换脸功能以及简单的图像风格转换，我们使用了GUI和网页等载体以便用户交互。
具体的项目介绍可以在`算分报告.pdf`中查看。

### 代码结构

`POSSION`文件夹包含了使用泊松编辑换脸的代码

`FSGAN`文件夹包含了使用对抗生成网络换脸的代码，基本上来自于论文原作者的</a href="https://github.com/YuvalNirkin/fsgan">实现</a>。注意我们没有上传网络的参数，若有需求请按照原作者项目中的流程向原作者申请，并按照其使用说明置于`FSGAN/fsgan/weights`内。

`webpage`文件夹包含了网页部分代码

`GUI.py`是GUI部分的代码

### 环境配置

对抗生成网络的环境要求请查看原作者的</a href="https://github.com/YuvalNirkin/fsgan">实现</a>

泊松图像编辑的环境要求：dlib, opencv-python(4.4.0.46), numpy

### 使用方法

这里只简单介绍网页以及GUI的使用。

#### 网页

下载本项目并解压后，进入`webpage`文件夹，运行`deal.py`和`app.py`，然后就可以在相应端口打开网页。

#### GUI

直接运行`GUI.py`即可。
