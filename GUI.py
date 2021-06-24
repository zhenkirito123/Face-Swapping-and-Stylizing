#team2  周慕歆 1900012994
#UI界面
import os
import io
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import cv2
import numpy as np
import random as rd
from PIL import Image
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk



root = tkinter.Tk()
w_box = 1280
h_box = 640
root.title('风格化')
root.geometry('1280x640')
e = tkinter.StringVar()
# print(e)
e_entry = tkinter.Entry(root,  textvariable=e)
e_entry.grid(row=6, column=1, padx=10, pady=5)

f = tkinter.StringVar()
# print(e)
f_entry = tkinter.Entry(root,  textvariable=f)
f_entry.grid(row=7, column=1, padx=10, pady=5)

q = tkinter.StringVar()#泊松合成
# print(e)
q_entry = tkinter.Entry(root,  textvariable=q)
q_entry.grid(row=9, column=1, padx=10, pady=5)

t = tkinter.StringVar()#save path
# print(e)
t_entry = tkinter.Entry(root,  textvariable=t)
t_entry.grid(row=8, column=1, padx=10, pady=5)
# print(e_entry.get())
# root.resizable(0,0)

submit_button = tkinter.Button(root, text="选择文件src", command=root.quit)
submit_button2 = tkinter.Button(root, text="选择文件dic", command=root.quit)
Label4 = tkinter.Label(root, text='保存图片的名称').grid(row=4, column=0)
p2 = tkinter.StringVar()
p2.set('000')


e4 = tkinter.Entry(root, textvariable=p2)
e4.grid(row=4, column=1, padx=10, pady=5)

anspic=''
savePath='D:/possion/result/000.jpg'
global imgGl
imgGl = tkinter.Label(root, image=None)
imgGl.place(x=300, y=0)


def resize(w_box, h_box, pil_image):
    w, h = pil_image.size
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def choose_file():
    selectFileName = filedialog.askopenfilename(title='选择文件')
    # print(selectFileName)
    e.set(selectFileName)
def choose_file2():
    selectFileName = filedialog.askopenfilename(title='选择文件')
    # print(selectFileName)
    f.set(selectFileName)
def choose_file3():#save_path
    selectFileName = filedialog.askdirectory()
    # print(selectFileName)
    t.set(selectFileName)
 
def showImg(img1):
    imgGl.config(image='')
    load = Image.open(img1)
    pil_image_resized = resize(w_box, h_box, load)
    render = ImageTk.PhotoImage(pil_image_resized)
    imgGl.image = render
    imgGl.config(image=render)

tkinter.Button(root, text="选择文件src", width=10, command=choose_file)\
    .grid(row=6, column=0, sticky=tkinter.W, padx=10, pady=5)
tkinter.Button(root, text="选择文件dic", width=10, command=choose_file2)\
    .grid(row=7, column=0, sticky=tkinter.W, padx=10, pady=5)
tkinter.Button(root, text="保存路径", width=10, command=choose_file3)\
    .grid(row=8, column=0, sticky=tkinter.W, padx=10, pady=5)

def mixture(img1_path,img2_path,save_path,save_name,sentence):
    q.set(sentence)
    a='python C:/Users/周慕歆/.vscode/UGATIT-pytorch-master-头像二次元/work.py'
    s=save_path+'/'+save_name
    cmd=str.format("%s \"%s\" \"%s\" \"%s\""%(a,img1_path,img2_path,s))
    os.system(cmd)    
    #os.system("python C:/Users/周慕歆/.vscode/UGATIT-pytorch-master-头像二次元/work.py D:/possion/data/3.jpg D:/possion/data/12.jpg D:/possion/result/000")    
def jiaoyan(img_path,snr=0.88):
    img=cv2.imread(img_path)
    h=img.shape[0]
    w=img.shape[1]
    img1=img.copy()
    sp=h*w   # 计算图像像素点个数
    NP=int(sp*(1-snr))   # 计算图像椒盐噪声点个数
    for i in range (NP):
        randx=np.random.randint(1,h-1)   # 生成一个 1 至 h-1 之间的随机整数
        randy=np.random.randint(1,w-1)   # 生成一个 1 至 w-1 之间的随机整数
        if np.random.random()<=0.5:   # np.random.random()生成一个 0 至 1 之间的浮点数
            img1[randx,randy]=0
        else:
            img1[randx,randy]=255
    cv2.imwrite(str('D:/possion/result/001.jpg'),img1)
    showImg('D:/possion/result/001.jpg')
    
def CarTon(image_path):
    image=cv2.imread(image_path)
    cartoon_image = cv2.stylization(image, sigma_s=150, sigma_r=0.25)  
    cv2.imwrite(str('D:/possion/result/002.jpg'),cartoon_image)
    showImg('D:/possion/result/002.jpg')
def CaiQian(image_path):
    image=cv2.imread(image_path)
    cartoon_image1, cartoon_image2  = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.5, shade_factor=0.02)  
    cv2.imwrite(str('D:/possion/result/003.jpg'),cartoon_image2)
    showImg('D:/possion/result/003.jpg')
def HeiBai(img_path):
    img=cv2.imread(img_path)
    h=img.shape[0]
    w=img.shape[1]
    img1=np.zeros((h,w),np.uint8)
    for i in range(h):
        for j in range(w):
            img1[i,j]=0.144*img[i,j,0]+0.587*img[i,j,1]+0.299*img[i,j,2]
    cv2.imwrite(str('D:/possion/result/004.jpg'),img1)
    showImg('D:/possion/result/004.jpg')
tkinter.Button(root, text="possion合成", width=10,command=lambda: mixture(e_entry.get(),f_entry.get(),t_entry.get(),p2.get(),"DONE"))\
    .grid(row=9, column=0, sticky=tkinter.W, padx=10, pady=5)

tkinter.Button(root, text="显示图片", width=10,command=lambda: showImg(savePath))\
    .grid(row=10, column=0, sticky=tkinter.W, padx=10, pady=5)

tkinter.Button(root, text="进行椒盐", width=10,command=lambda: jiaoyan(savePath))\
    .grid(row=11, column=0, sticky=tkinter.W, padx=10, pady=5)
 
tkinter.Button(root, text="进行卡通", width=10,command=lambda: CarTon(savePath))\
    .grid(row=12, column=0, sticky=tkinter.W, padx=10, pady=5)

tkinter.Button(root, text="进行彩铅", width=10,command=lambda: CaiQian(savePath))\
    .grid(row=13, column=0, sticky=tkinter.W, padx=10, pady=5)

tkinter.Button(root, text="进行黑白", width=10,command=lambda: HeiBai(savePath))\
    .grid(row=14, column=0, sticky=tkinter.W, padx=10, pady=5)

tkinter.mainloop()

'''
def select1():
    x=radio1.get()
    if x==1:
        lb.config(text='请在下面两个框里选择要合成的人脸图片')
    else:
        lb.config(text='请在第一个框里选择要风格化的图片')
root=Tk()
root.geometry('1200x800')
radio1=IntVar()
lb1=Label(text='选择是否用泊松或GAN合成人脸')
lb1.pack()

r1=Radiobutton(root,text='yes',variable=radio1,value=1,command=select1)
r1.pack(anchor=W)

r2=Radiobutton(root,text='no',variable=radio1,value=0,command=select1)
r2.pack(anchor=W)

lb=Label(root)
lb.pack()

#选择图片
default_path='C:\\Users\\周慕歆\\Desktop\\xinxin.png'
pic1_path=filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_path)))

root.mainloop()

'''




class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        
        #选择图片
        #点击button
        #显示处理后的图片
        
        #设置window的参数
        self.resize(1200, 800)
        self.move(500, 200)
        self.setWindowTitle('enjoyGAN')
        self.setWindowIcon(QIcon('C:\\Users\\周慕歆\\Desktop\\enjoyGAN.jpg')) # 创建一个QIcon对象并接收一个我们要显示的图片路径作为参数
        palette = QPalette()#背景图片
        backpic=QPixmap('C:\\Users\\周慕歆\\Desktop\\orange.jpg')
        backpic = backpic.scaled(self.width(),self.height())
        palette.setBrush(QPalette.Background,QBrush(backpic))
        self.setPalette(palette)

        self.tarpic=None  #要操作的图片
        self.rtpic=None   #操作完传送回来的图片
        self.inpic()  #先读入目标图片tarpic
        
        #添加风格化选项--单选按钮
        layout=QHBoxLayout()#实例化一个布局
        
        self.btn1=QRadioButton('椒盐')
        self.btn1.toggled.connect(lambda: self.buttonState(self.btn1))# toggled信号代表切换
        layout.addWidget(self.btn1)

        self.btn2 = QRadioButton("卡通")
        self.btn2.toggled.connect(lambda:self.buttonState(self.btn2))
        layout.addWidget(self.btn2)

        self.btn4 = QRadioButton("泊松")
        self.btn4.toggled.connect(lambda:self.buttonState(self.btn4))
        layout.addWidget(self.btn4)

        self.btn5 = QRadioButton("彩铅")
        self.btn5.toggled.connect(lambda:self.buttonState(self.btn5))
        layout.addWidget(self.btn5)

        self.btn6 = QRadioButton("GAN")
        self.btn6.toggled.connect(lambda:self.buttonState(self.btn6))
        layout.addWidget(self.btn6)

        self.btn3=QPushButton('确认')
        self.btn3.setCheckable(True)
        self.btn3.clicked.connect(lambda:self.showpic())
        layout.addWidget(self.btn3)

        self.setLayout(layout)

        self.lbrp=QLabel(self)#label return picture
        self.lbrp.setGeometry(600,30,360,360)
        self.lbrp.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
        
        
    def showpic(self):
        if self.btn3.isChecked() == True:
            print('开始显示图片')
            if self.rtpic is None:
                print("返回的图片为空")
                pix=QPixmap('C:\\Users\\周慕歆\\Desktop\\xinxin.png')
            else:
                pix=QPixmap(self.rtpic)

            self.lbrp.setPixmap(pix)
    def buttonState(self,btn):
        #qtpixmap to cv2
        xpic=self.tarpic
        qimg = xpic.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        pil_im = result[..., :3]
        
        #pil_im=self.tarpic
        if btn.text() == "椒盐":
            if btn.isChecked() == True:
                rt=JiaoYan123(pil_im,self.label.width(), self.label.height())
                print('椒盐运行结束')
                #cv2 to qpixmap
                height, width, depth = rt.shape
                cvimg = cv2.cvtColor(rt, cv2.COLOR_BGR2RGB)
                cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
                self.rtpic=QtGui.QPixmap(cvimg)
                return
        if btn.text() == "卡通":
            if btn.isChecked() == True:
                rt=CarTon123(pil_im)
                print('卡通运行结束')
                #cv2 to qpixmap
                height, width, depth = rt.shape
                cvimg = cv2.cvtColor(rt, cv2.COLOR_BGR2RGB)
                cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
                self.rtpic=QtGui.QPixmap(cvimg)
                return
        if btn.text() == "泊松":
            if btn.isChecked() == True:
                rt=BoSong123(pil_im)
                print('泊松运行结束')
                #cv2 to qpixmap
                #height, width, depth = rt.shape
                #cvimg = cv2.cvtColor(rt, cv2.COLOR_BGR2RGB)
                #cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
                #self.rtpic=QtGui.QPixmap(cvimg)
                #return
                
        if btn.text() == "彩铅":
            if btn.isChecked() == True:
                rt=CaiQian123(pil_im)
                print('彩铅运行结束')
                #cv2 to qpixmap
                height, width, depth = rt.shape
                cvimg = cv2.cvtColor(rt, cv2.COLOR_BGR2RGB)
                cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
                self.rtpic=QtGui.QPixmap(cvimg)
                return
        if btn.text() == "GAN":
            if btn.isChecked() == True:
                rt=Gan123(pil_im)
                print('GAN运行结束')
                #cv2 to qpixmap
                #height, width, depth = rt.shape
                #cvimg = cv2.cvtColor(rt, cv2.COLOR_BGR2RGB)
                #cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
                #self.rtpic=QtGui.QPixmap(cvimg)
                #return
                
    def inpic(self):
        self.label=QLabel(self)
        self.label.setText('选择图片')
        self.label.setFixedSize(360, 360)
        self.label.move(10, 30)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(10, 30)
        btn.clicked.connect(self.openimage)
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        self.tarpic=jpg
        

def JiaoYan123(img,w,h,snr=0.88):
    
    #添加椒盐噪声
    #prob:噪声比例 s
    
    h=img.shape[0]
    w=img.shape[1]
    img1=img.copy()
    sp=h*w   # 计算图像像素点个数
    NP=int(sp*(1-snr))   # 计算图像椒盐噪声点个数
    for i in range (NP):
        randx=np.random.randint(1,h-1)   # 生成一个 1 至 h-1 之间的随机整数
        randy=np.random.randint(1,w-1)   # 生成一个 1 至 w-1 之间的随机整数
        if np.random.random()<=0.5:   # np.random.random()生成一个 0 至 1 之间的浮点数
            img1[randx,randy]=0
        else:
            img1[randx,randy]=255
    return img1

def HeiBai123(img):
    if img is None:
        print('黑白照片为空')
        return 
    else:
        h=img.shape[0]
        w=img.shape[1]
        img1=np.zeros((h,w),np.uint8)
        for i in range(h):
            for j in range(w):
                img1[i,j]=0.144*img[i,j,0]+0.587*img[i,j,1]+0.299*img[i,j,2]
        return img1   
def CarTon123(image):
    cartoon_image = cv2.stylization(image, sigma_s=150, sigma_r=0.25)  
    return cartoon_image
def BoSong123(image):
    print('posion editing')
def CaiQian123(image):
    cartoon_image1, cartoon_image2  = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.5, shade_factor=0.02)  
    return cartoon_image2
def Gan123(image):
    print('GAN editing')

        
