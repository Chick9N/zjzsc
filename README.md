# zjzsc
Python自动生成证件照
此py在3.7.9下运行
你需要安装的库：paddlepaddle paddlehub（先后安装）;win32ui;PyQt5;pillow;opencv2及其tools
paddlepaddle安装的模型：hub install deeplabv3p_xception65_humanseg==1.0.0

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
