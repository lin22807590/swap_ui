import sys
import re
import os
from PyQt5 import uic  # , QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QMessageBox, QStatusBar
from PyQt5 import QtCore  # , QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize, QModelIndex
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
from tableview import FR_Delegate, FR_Model, FR_TableView

from collections import namedtuple
from imgWindow import ImageWindow
# Create a custom namedtuple class to hold our data.
timage = namedtuple("timage", "id title image")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('face_reenact.ui', self)  # Load the .ui file
        self.setWindowTitle("Face Reenactment")
        self.action_Quit.triggered.connect(lambda: quit())
        self.action_Source_Images.triggered.connect(self.sourceImages)
        self.action_Moab.triggered.connect(self.moab)

        self.model = FR_Model()
        self.delegate = FR_Delegate(self.uwidget.size())
        self.tview = FR_TableView(self)
        self.tview.setGridStyle(Qt.NoPen)
        self.tview.setModel(self.model)
        self.tview.setItemDelegate(self.delegate)

        layout = QVBoxLayout()
        layout.addWidget(self.tview)
        self.uwidget.setLayout(layout)

    def sourceImages(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory",
            ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        srcImgs = ImageWindow(None, dir, 1)
        srcImgs.show()

    def moab(self):
        self.tview.doMoab()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()
