from numpy import maximum
from PyQt5 import QtCore 
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap

import cv2
import time
import os

from UI import Ui_MainWindow
from img_controller import img_controller
from img_controller2 import img_controller2
from test import output_order

class MainWindow_controller(QMainWindow):
    combovalue1 =0
    combovalue2 =0
    msgstart=0
    msgend=0
    output_path =''
    

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #print(self.ui.comboBox.currentText())
        self.setup_control()
        self.ui.btn_startend.clicked.connect(self.set_start_end)
        self.ui.btn_driving_video.clicked.connect(self.select_driving_video)
        #choices = ['1', '101','156', '201', '301', '401']
        #self.ui.comboBox.addItems(choices)
        #self.ui.comboBox.currentIndexChanged.connect(self.displaycombobox)
        #self.displaycombobox()
        #self.displayslider()
        self.ui.slider_siximg.setMinimum(1)
        self.ui.slider_siximg.setMaximum(469)
        print("repeat")
        self.ui.slider_siximg.valueChanged.connect(self.displayslider)
        self.displayslider()
        self.ui.execute_Button.clicked.connect(self.execute)
        #self.ui.label_slider.setText(f'你目前瀏覽的是： 到 ')
        self.ui.btn_output.clicked.connect(self.select_output_folder)
        #print(self.driving_video_path)
        
    def setup_control(self):
        self.file_path = ''
        self.img_controller = img_controller(img_path=self.file_path,
                                             label_img=self.ui.label_img,
                                             label_file_path=self.ui.label_file_name,
                                             label_ratio=self.ui.label_ratio,
                                             label_img_shape=self.ui.label_img_shape)

        self.ui.btn_open_file.clicked.connect(self.open_file)         
        self.ui.btn_zoom_in.clicked.connect(self.img_controller.set_zoom_in)
        self.ui.btn_zoom_out.clicked.connect(self.img_controller.set_zoom_out)
        self.ui.slider_zoom.valueChanged.connect(self.getslidervalue)
        
    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Open file", ".\\") # start path        
        self.init_new_picture(filename)

    def init_new_picture(self, filename):
        self.ui.slider_zoom.setProperty("value", 50)
        self.img_controller.set_path(filename)        

    def getslidervalue(self):        
        self.img_controller.set_slider_value(self.ui.slider_zoom.value()+1)
    
    def displaycombobox(self):
        self.ui.label_combobox.setText(f'你目前選擇的是第：%s 到 {int(self.ui.comboBox.currentText())+5} 張照片' % self.ui.comboBox.currentText()  )
        self.displaysiximgs()
    
    def displayslider(self):
        self.ui.label_slider.setText(f'你目前瀏覽的是第：%s 到 {int(self.ui.slider_siximg.value())+5} 張照片' % self.ui.slider_siximg.value()  )
        self.displaysiximgs()
    
    def displaysiximgs(self):
        imgstart=1
        '''if(self.combovalue1 != int(self.ui.comboBox.currentText())):
            imgstart=int(self.ui.comboBox.currentText())
            self.combovalue1 = int(self.ui.comboBox.currentText())'''
        if(self.combovalue2 != self.ui.slider_siximg.value()):
            imgstart=int(self.ui.slider_siximg.value())
            self.combovalue2 = int(self.ui.slider_siximg.value())
        try:
            self.img_path_2 = f'{self.driving_video_path}\\image_{str(imgstart).zfill(4)}.jpg'
            self.img_path_3 = f'{self.driving_video_path}\\image_{str(imgstart+1).zfill(4)}.jpg'
            self.img_path_4 = f'{self.driving_video_path}\\image_{str(imgstart+2).zfill(4)}.jpg'
            self.img_path_5 = f'{self.driving_video_path}\\image_{str(imgstart+3).zfill(4)}.jpg'
            self.img_path_6 = f'{self.driving_video_path}\\image_{str(imgstart+4).zfill(4)}.jpg'
            self.img_path_7 = f'{self.driving_video_path}\\image_{str(imgstart+5).zfill(4)}.jpg'
        except:
            self.img_path_2 = f'D:\\program\\ui\\03\\image_{str(imgstart).zfill(4)}.jpg'
            self.img_path_3 = f'D:\\program\\ui\\03\\image_{str(imgstart+1).zfill(4)}.jpg'
            self.img_path_4 = f'D:\\program\\ui\\03\\image_{str(imgstart+2).zfill(4)}.jpg'
            self.img_path_5 = f'D:\\program\\ui\\03\\image_{str(imgstart+3).zfill(4)}.jpg'
            self.img_path_6 = f'D:\\program\\ui\\03\\image_{str(imgstart+4).zfill(4)}.jpg'
            self.img_path_7 = f'D:\\program\\ui\\03\\image_{str(imgstart+5).zfill(4)}.jpg'

        self.img_controller2 = img_controller2(img_path_2=self.img_path_2,
                                                label_img_2=self.ui.label_img_2,
                                                img_path_3=self.img_path_3,
                                                label_img_3=self.ui.label_img_3,
                                                img_path_4=self.img_path_4,
                                                label_img_4=self.ui.label_img_4,
                                                img_path_5=self.img_path_5,
                                                label_img_5=self.ui.label_img_5,
                                                img_path_6=self.img_path_6,
                                                label_img_6=self.ui.label_img_6,
                                                img_path_7=self.img_path_7,
                                                label_img_7=self.ui.label_img_7)
        
    def open_file2(self):
        filename2, filetype = QFileDialog.getOpenFileName(self, "Open file", ".\\") # start path        
        self.init_new_picture_six(filename2)
        self.img_controller2.set_path(filename2)    

    def select_output_folder(self):
        output_path = QFileDialog.getExistingDirectory(self, "Open folder", ".\\")                 # start path
        #print(output_path)
        self.ui.label_output_path.setText(f"Output path = {output_path}")
        self.output_path=output_path

    def set_start_end(self):
        self.msgstart = int(self.ui.lineEdit_start.text())
        self.msgend = int(self.ui.lineEdit_end.text())
        
        self.ui.label_startend.setText(f'起點={int(self.msgstart)}, 終點={int(self.msgend)}')

    def select_driving_video(self):
        driving_video_path=QFileDialog.getExistingDirectory(self, "Open folder", ".\\")
        self.ui.label_driving_video_path.setText(f"Driving video path = {driving_video_path}")
        self.driving_video_path=driving_video_path
        self.find_maximum()
        #print(f'{self.driving_video_path}')

    def find_maximum(self):
        self.drvmax=0
        initial_count = 0
        dir=self.driving_video_path
        try:
            for path in os.listdir(dir):
                if os.path.isfile(os.path.join(dir,path)):
                    initial_count+=1
            self.drvmax = initial_count-5
            self.ui.slider_siximg.setMaximum(self.drvmax)
        except:
            print("0")
        print(initial_count)
        
        print(self.drvmax)



    def execute(self):
        self.input=self.img_controller.img_path
        self.driving_video=self.driving_video_path
        self.output=self.output_path
        self.start=int(self.msgstart)
        self.end=int(self.msgend)
        self.test=output_order(input=self.input, driving_video=self.driving_video,output=self.output, start=self.start, end=self.end)
        #print(f'-i {self.img_controller.img_path} -o {self.output_path} -s {int(self.ui.comboBox.currentText())} -e ' )
    