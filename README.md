# Facebrain

facebrain是一个用深度学习进行人脸识别的python api. 

人脸识别采用facenet，见paper: ["FaceNet: A Unified Embedding for Face Recognition and Clustering"](http://arxiv.org/abs/1503.03832).

人脸检测采用MTCNN, 见paper: ["Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks"](https://kpzhang93.github.io/MTCNN_face_detection_alignment/).

模型由开源项目[facenet](https://github.com/davidsandberg/facenet)提供.

## 预训练模型
人脸识别模型为inception_resnet_v1, 在[MS-Celeb-1M](https://www.microsoft.com/en-us/research/project/ms-celeb-1m-challenge-recognizing-one-million-celebrities-real-world/) 训练完成, 准确率达到0.992.

在自己的数据集上训练模型参见github项目[facenet](https://github.com/davidsandberg/facenet)

预训练模型下载地址[inception_resnet_v1](https://pan.baidu.com/s/1eTooi9k). 下载解压后放到facebrain目录下.

## 结构
![image](https://github.com/CoderSLZhang/Facebrain/blob/master/facebrain_architecture.jpg)

## 使用
使用前需要安装tensorflow, numpy, scipy, cv2

1. 引入
```
from facebrain.facebrain import Facebrain
```
2. 创建facebrain实例
```
face_brain = Facebrain(face_size=(150, 150))
```
3. 读取图片
```
tfboys_img = face_brain.read_image(file)
```
file可以是一个路径或是一个file object

4. 人脸检测
```
tfboys_faces, tfboys_boxes = face_brain.detect_faces(tfboys_img)
```
5. 人脸编码
```
tfboys_encoding = face_brain.encode_faces(tfboys_faces)
```
6. 人脸对比

比较人脸编码的相似度，越小越相似
```
face_brain.compare_faces(tfboys_encoding[0], database_encodings)
```
当人脸编码相似度小于threshold 0.7时判断为同一个人
```
face_brain.recognize_face(tfboys_encoding[0], database_encodings, threshold=0.7)
```
*具体使用参见demo中的jupyter notebook* 

## Demo
### jupyther-notebook
人脸检测，人脸识别，人脸提取，人脸识别

![image](https://github.com/CoderSLZhang/Facebrain/blob/master/demo/demo2.png)
### iOS 人脸识别
需要启动face_server.py，配置好iOS项目ip和端口

![image](https://github.com/CoderSLZhang/Facebrain/blob/master/demo/demo1.jpg)
