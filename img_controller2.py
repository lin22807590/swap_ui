from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap

import cv2

class img_controller2(object):
    def __init__(self, img_path_2, label_img_2, img_path_3, label_img_3, img_path_4, label_img_4,img_path_5, label_img_5, img_path_6, label_img_6, img_path_7, label_img_7):
        self.img_path_2 = img_path_2
        self.label_img_2= label_img_2
        self.img_path_3 = img_path_3
        self.label_img_3= label_img_3
        self.img_path_4 = img_path_4
        self.label_img_4= label_img_4
        self.img_path_5 = img_path_5
        self.label_img_5= label_img_5
        self.img_path_6 = img_path_6
        self.label_img_6= label_img_6
        self.img_path_7 = img_path_7
        self.label_img_7= label_img_7

        self.display_img2()
        self.display_img3()
        self.display_img4()
        self.display_img5()
        self.display_img6()
        self.display_img7()

    
    
    def display_img2(self):
        self.img2 = cv2.imread(self.img_path_2)
        self.img2 = cv2.resize(self.img2, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img2.shape
        bytesPerline2 = 3 * width
        self.qimg2 = QImage(self.img2, width, height, bytesPerline2, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap2 = QPixmap.fromImage(self.qimg2)
        self.qpixmap_height2 = self.qpixmap2.height()
        self.label_img_2.setPixmap(QPixmap.fromImage(self.qimg2))

    
    def display_img3(self):
        self.img3 = cv2.imread(self.img_path_3)
        self.img3 = cv2.resize(self.img3, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img3.shape
        bytesPerline3 = 3 * width
        self.qimg3 = QImage(self.img3, width, height, bytesPerline3, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap3 = QPixmap.fromImage(self.qimg3)
        self.qpixmap_height3 = self.qpixmap3.height()
        self.label_img_3.setPixmap(QPixmap.fromImage(self.qimg3))

    def display_img4(self):
        self.img4 = cv2.imread(self.img_path_4)
        self.img4 = cv2.resize(self.img4, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img4.shape
        bytesPerline4 = 3 * width
        self.qimg4 = QImage(self.img4, width, height, bytesPerline4, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap4 = QPixmap.fromImage(self.qimg4)
        self.qpixmap_height4 = self.qpixmap4.height()
        self.label_img_4.setPixmap(QPixmap.fromImage(self.qimg4))

    def display_img5(self):
        self.img5 = cv2.imread(self.img_path_5)
        self.img5 = cv2.resize(self.img5, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img5.shape
        bytesPerline5 = 3 * width
        self.qimg5 = QImage(self.img5, width, height, bytesPerline5, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap5 = QPixmap.fromImage(self.qimg5)
        self.qpixmap_height5 = self.qpixmap5.height()
        self.label_img_5.setPixmap(QPixmap.fromImage(self.qimg5))

    def display_img6(self):
        self.img6 = cv2.imread(self.img_path_6)
        self.img6 = cv2.resize(self.img6, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img6.shape
        bytesPerline6 = 3 * width
        self.qimg6 = QImage(self.img6, width, height, bytesPerline6, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap6 = QPixmap.fromImage(self.qimg6)
        self.qpixmap_height6 = self.qpixmap6.height()
        self.label_img_6.setPixmap(QPixmap.fromImage(self.qimg6))

    def display_img7(self):
        self.img7 = cv2.imread(self.img_path_7)
        self.img7 = cv2.resize(self.img7, (480, 270), interpolation=cv2.INTER_AREA)
        height, width, channel = self.img7.shape
        bytesPerline7 = 3 * width
        self.qimg7 = QImage(self.img7, width, height, bytesPerline7, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap7 = QPixmap.fromImage(self.qimg7)
        self.qpixmap_height7 = self.qpixmap7.height()
        self.label_img_7.setPixmap(QPixmap.fromImage(self.qimg7))
    


        