# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mdisk/FaceProj/swap_ui/ImgTool/newImage.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(483, 349)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qimage = QtWidgets.QLabel(Dialog)
        self.qimage.setObjectName("qimage")
        self.verticalLayout.addWidget(self.qimage)
        self.degree = QtWidgets.QScrollBar(Dialog)
        self.degree.setMinimum(-180)
        self.degree.setMaximum(180)
        self.degree.setSingleStep(1)
        self.degree.setOrientation(QtCore.Qt.Horizontal)
        self.degree.setObjectName("degree")
        self.verticalLayout.addWidget(self.degree)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.qimage.setText(_translate("Dialog", "TextLabel"))