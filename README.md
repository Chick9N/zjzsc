# zjzsc
项目名：Python自动生成证件照
Python版本：3.7.X
依赖：
深度学习模型：pip install paddlepaddle;pip install paddlehub;hub install deeplabv3p_xception65_humanseg==1.0.0;
UI:pip install win32ui;pip install PyQt5;pip install pillow;pip install opencv-python;pip install opencv-contrib-python==4.5.3.56

图像处理思路：
利用humanseg深度模型剥离人像→
利用cv2人脸识别模型识别人脸并找到中心点→
根据1寸/2寸照片纵横比反推需要裁剪的图片区域→
利用pillow库按照坐标进行裁剪→
利用cv2库遍历全像素点并填充透明像素点为底色→
保存图像至.py文件所在文件夹→
利用pillow库显示生成好的证件照。

注：
此程序单次只能生成一个证件照

UI图：
![zjzsc](https://user-images.githubusercontent.com/88222209/135122015-a1e3a286-1961-4e18-9eff-4d4054c6e178.png)

效果：
![原图](https://user-images.githubusercontent.com/88222209/135122157-57704ff4-cf14-47f5-9aea-ec5ea42dede0.jpg)
![效果图](https://user-images.githubusercontent.com/88222209/135122163-8ddcd7c8-9643-4292-b49a-788f0f82707f.png)
