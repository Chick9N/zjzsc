import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QFrame
from PyQt5.QtGui import QIcon
import ctypes  # 图标
import sys
import win32ui
import paddlehub as hub
import cv2
from PIL import Image


global img, color, size


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("证件照生成")  # 标题

        self.setGeometry(400, 400, 250, 300)  # 窗体位置和大小
        self.setFixedSize(250, 300)  # 固定大小

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('icon.png')
        self.setWindowIcon(QIcon('icon.png'))

        # 导入照片的按钮
        self.button1 = QPushButton("请选择您的照片", self)
        self.button1.move(25, 25)  # 位置
        self.button1.clicked.connect(getpath)

        # 选择尺寸的下拉列表
        frame1 = QFrame(self)
        frame1.move(25, 70)
        label1 = QLabel('尺寸', frame1)
        label1.move(0, 3)
        combobox1 = QComboBox(frame1)
        combobox1.move(30, 0)
        combobox1.addItem('')
        combobox1.addItem('1寸')
        combobox1.addItem('2寸')
        combobox1.activated[str].connect(self.combo1Activated)

        # 选择照片底色的下拉列表
        frame2 = QFrame(self)
        frame2.move(25, 115)
        label2 = QLabel('照片底色', frame2)
        label2.move(0, 3)
        combobox2 = QComboBox(frame2)
        combobox2.move(55, 0)
        combobox2.addItem('')
        combobox2.addItem('白')
        combobox2.addItem('蓝')
        combobox2.addItem('红')
        combobox2.activated[str].connect(self.combo2Activated)

        # 开始按钮
        self.button2 = QPushButton("开始生成证件照", self)
        self.button2.move(25, 160)  # 位置
        self.button2.clicked.connect(ImgProcess)

        # 警告1
        self.label3 = QLabel('*未选择文件！', self)
        self.label3.setStyleSheet('color:red')
        self.label3.move(140, 30)

        # 警告2
        self.label4 = QLabel('*未选择尺寸！', frame1)
        self.label4.setStyleSheet('color:red')
        self.label4.move(115, 3)

        # 警告3
        self.label5 = QLabel('*未选择底色！', frame2)
        self.label5.setStyleSheet('color:red')
        self.label5.move(115, 3)

        # 成功提示
        self.label6 = QLabel('', self)
        self.label6.setStyleSheet('color:green')
        self.label6.move(140, 163)

        # 注意事项
        self.label7 = QLabel('注意：', self)
        self.label7.setStyleSheet('color:blue')
        self.label7.move(25, 205)
        self.label8 = QLabel('1.图片文件路径不要出现中文', self)
        self.label8.setStyleSheet('color:blue')
        self.label8.move(25, 225)
        self.label9 = QLabel('2.不要选择含多人照片', self)
        self.label9.setStyleSheet('color:blue')
        self.label9.move(25, 245)
        self.label10 = QLabel('3.建议照片人脸居中且照入胸部以上', self)
        self.label10.setStyleSheet('color:blue')
        self.label10.move(25, 265)

        self.show()

    @staticmethod
    def combo1Activated(s):
        global size
        if s == '1寸':
            size = 1
            window.label4.setStyleSheet('color:green')
            window.label4.setText('*当前尺寸为：1寸')
            window.label4.adjustSize()
        elif s == '2寸':
            size = 2
            window.label4.setStyleSheet('color:green')
            window.label4.setText('*当前尺寸为：2寸')
            window.label4.adjustSize()
        else:
            window.label4.setStyleSheet('color:red')
            window.label4.setText('*未选择尺寸！')
            window.label4.adjustSize()

    @staticmethod
    def combo2Activated(s):
        global color
        color = s
        if color == '白':
            window.label5.setStyleSheet('color:green')
            window.label5.setText('*当前颜色为：白色')
            window.label5.adjustSize()
        elif color == '蓝':
            window.label5.setStyleSheet('color:green')
            window.label5.setText('*当前颜色为：蓝色')
            window.label5.adjustSize()
        elif color == '红':
            window.label5.setStyleSheet('color:green')
            window.label5.setText('*当前颜色为：红色')
            window.label5.adjustSize()
        else:
            window.label5.setStyleSheet('color:red')
            window.label5.setText('*未选择底色！')
            window.label5.adjustSize()


def getpath():  # 用来获取图片路径path的函数
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir('')  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    global img1
    img1 = os.path.abspath(dlg.GetPathName())  # 获取选择的照片的路径
    # 判断是否为图片类型
    tail = os.path.splitext(img1)[1]
    if os.path.exists(img1) and (tail == '.img' or tail == '.png' or tail == '.jpeg' or tail == '.jpg'):
        window.label3.setStyleSheet('color:green')
        window.label3.setText('*照片选择成功')
    else:
        window.label3.setStyleSheet('color:red')
        window.label3.setText('*不支持的文件类型！')


def ImgProcess():
    if os.path.exists(r'humanseg_output'):
        for i in os.listdir(r'humanseg_output'):
            pic1 = r'humanseg_output' + "//" + i
            if os.path.isfile(pic1):
                os.remove(pic1)
                pic1 = None

    # 剥离人像
    imgs = []
    imgs.append(img1)
    humanseg = hub.Module(name='deeplabv3p_xception65_humanseg')
    humanseg.segmentation(data={'image': imgs})

    # 识别人脸
    humanbody = os.listdir('humanseg_output')
    b = humanbody[0]
    # path1就是要处理的图片
    path1 = r'humanseg_output/' + b
    img2 = cv2.imread(path1)
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(gray)
    result = []  # 存坐标用
    for (x0, y0, width, height) in faces:
        result.append((x0, y0, x0 + width, y0 + height))
    centerx = x0 + width // 2
    centery = y0 + height // 2

    # 获取人脸中心坐标和截取区域坐标
    im = Image.open(path1)
    h = im.height
    w = im.width
    # 左上角坐标
    if size == 1:
        ratio = 1.4  # 413 / 295
    if size == 2:
        ratio = 1.5  # 626 / 416
    x1 = centerx - height
    y1 = centery - int(height * ratio)
    # 右下角坐标(开区间
    x2 = centerx + height
    y2 = centery + int(height * ratio)
    # 防止超坐标
    if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
        minx = [centerx, w - centerx]
        miny = [centery, h - centery]
        _minx = min(minx)
        _miny = min(miny)
        if _miny / ratio <= _minx:
            x1 = centerx - _miny / ratio
            y1 = centery - _miny
            x2 = centerx + _miny / ratio
            y2 = centery + _miny
        else:
            x1 = centerx - _minx
            y1 = centery - _minx * ratio
            x2 = centerx + _minx
            y2 = centery + _minx * ratio


    # 按坐标截取
    cut = im.crop((x1, y1, x2, y2))
    cut.save('cut.png')

    # 按尺寸缩小图像
    im = Image.open(r'cut.png')
    if size == 1:
        myresized = im.resize((295, 413))
    else:
        myresized = im.resize((413, 626))
    myresized.save('resized.png')

    # 决定背景颜色
    if color == '白':
        b, g, r, a = 255, 255, 255, 255
    elif color == '蓝':
        b, g, r, a = 219, 142, 67, 255
    else:
        b, g, r, a = 0, 0, 255, 255

    im = cv2.imread(r'resized.png', cv2.IMREAD_UNCHANGED)

    for x in range(im.shape[0]):  # 图片的高
        for y in range(im.shape[1]):  # 图片的宽
            px = im[x, y]
            if px[3] <= 215:  # 填充完全及部分透明像素
                im[x, y] = [b, g, r, a]
    cv2.imwrite('zjz.png', im)

    if os.path.exists(r'zjz.png'):
        window.label6.setText('*证件照生成成功')
        window.label6.adjustSize()
        im = Image.open(r'zjz.png')
        im.show()


if __name__ == '__main__':
    # 运行窗体
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()
