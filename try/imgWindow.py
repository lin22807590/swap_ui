import glob
import math
import os, sys
from collections import namedtuple

from PyQt5 import uic, QtCore #, QtWidgets 
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtWidgets import QVBoxLayout
# Create a custom namedtuple class to hold our data.
preview = namedtuple("preview", "id title image")

IMAGEFILESPATH = "/home/mdisk/FaceProj/images/Wash/Wash-boy"
#IMAGEFILESPATH = "imgs"
NUMBER_OF_COLUMNS = 4
CELL_PADDING = 2 # all sides
class PreviewDelegate(QStyledItemDelegate):

    def __init__(self, width, cols):
        super().__init__()
        # .data holds our data for display, as a list of Preview objects.
        self.width = width
        self.cols = cols

    def setParas(self, width, cols):
        self.width = width
        self.cols = cols

    def paint(self, painter, option, index):

        data = index.model().data(index, Qt.DisplayRole)
        if data is None:
            return
        dataImg = data.image

        width = option.rect.width() - CELL_PADDING * 2
        height = option.rect.height() - CELL_PADDING * 2

        # option.rect holds the area we are painting on the widget (our table cell)
        # scale our pixmap to fit
        scaled = dataImg.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
        # Position in the middle of the area.
        x = CELL_PADDING + (width - scaled.width()) / 2
        y = CELL_PADDING + (height - scaled.height()) / 2

        painter.drawImage(int(option.rect.x() + x), int(option.rect.y() + y), scaled)
        
    def sizeHint(self, option, index):
        # All items the same size.
        w = int(0.95*self.width/self.cols)
        h = int(w*1080/1920)

        return QSize(w, h)


class PreviewModel(QAbstractTableModel):
    def __init__(self, cols=NUMBER_OF_COLUMNS):
        super().__init__()
        # .data holds our data for display, as a list of Preview objects.
        self.previews = []
        self.cols = cols

    def setCols(self, cols):
        self.cols = cols
        self.layoutChanged.emit()

    def data(self, index, role):
        try:
            data = self.previews[index.row() * self.cols + index.column() ]
        except IndexError:
            # Incomplete last row.
            return
            
        if role == Qt.DisplayRole:
            return data   # Pass the data to our delegate to draw.
           
        if role == Qt.ToolTipRole:
            return os.path.basename(data.title)

    def columnCount(self, index):
        return self.cols

    def rowCount(self, index):
        n_items = len(self.previews)
        return math.ceil(n_items / self.cols)


class ImageWindow(QMainWindow):
    def __init__(self, parent, folder, kind):
        super().__init__()
        self.up = parent
        self.folder = folder
        uic.loadUi('imgWindow.ui', self) # Load the .ui file
        self.setWindowTitle(self.folder)
        self.cols = NUMBER_OF_COLUMNS
        self.tview = QTableView()
        self.tview.horizontalHeader().hide()
        self.tview.verticalHeader().hide()
        self.tview.setGridStyle(Qt.NoPen)
        
        mw, mh = self.width(), self.height()
        self.delegate = PreviewDelegate(mw, self.cols)
        self.tview.setItemDelegate(self.delegate)
        self.model = PreviewModel()
        self.tview.setModel(self.model)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tview)
        self.uwidget.setLayout(layout)

        # Connection
        self.bdec.clicked.connect(self.decrease)
        self.binc.clicked.connect(self.increase)
        self.bOffset.clicked.connect(self.setOffset)
        self.imgOffset.valueChanged.connect(self.offsetChanged)
        self.imgOffset.sliderReleased.connect(self.offsetReleased)
        self.tview.clicked.connect(self.imgClicked)
        self.loadFiles()

        # Variation
        if kind == 1:
            self.bMarkA.hide()
            self.bMarkB.hide()
            self.bSrcFile.clicked.connect(self.setSrcFile)

    def setSrcFile(self):
        if self.clickFile:
            self.up.srcFile = self.clickFile
            self.up.tSrcFile.setText(f"Source File = {self.clickFile}")

    def imgClicked(self, index):
        offset = index.row() * self.cols + index.column()
        self.clickPos = self.imgOffset.value() + offset
        data = self.model.previews[offset]
        self.clickFile = data.title
        sizeText = f"Image Size: ({data.image.width()}, {data.image.height()})"
        posText = f"Clicked: {self.clickPos}"
        self.info.setText(sizeText+"  "+posText)

    def loadFiles(self):
        self.files = glob.glob(f"{self.folder}/*.jpg")
        self.files.sort()
        if len(self.files) > 100:
            self.imgOffset.setRange(0, len(self.files)-100)
            self.imgOffset.setValue(0)
        else:
            self.imgOffset.hide()
            self.imgSRLabel.hide()

        self.loadImages(0)
        self.show() # Show the GUI
        self.uwidget.update()

    def offsetChanged(self, value):
        self.imgSRLabel.setText(f"Offset: {value:04d}")

    def setOffset(self):
        self.loadImages(self.clickPos)
        self.imgOffset.setValue(self.clickPos)
        idx = self.model.index(0,0)
        self.tview.scrollTo(idx)
        self.tview.setCurrentIndex(idx)

    def offsetReleased(self):
        self.imgOffset.setValue(self.imgOffset.value())
        self.loadImages(self.imgOffset.value())

    def loadImages(self, offset):
        rightidx = min(len(self.files), offset+100)
        # Add a bunch of images.
        self.model.previews = []
        for n, fn in enumerate(self.files[offset:rightidx]):
            image = QImage(fn)
            if n == 0:
                self.info.setText(f"Image Size: ({image.width()}, {image.height()})")
            item = preview(n, fn, image)
            self.model.previews.append(item)

        self.model.layoutChanged.emit()
        
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()

    def decrease(self):
        if self.cols > 1:
            self.cols = self.cols - 1
            self.model.setCols(self.cols)
            mw, mh = self.width(), self.height()
            self.delegate.setParas(mw, self.cols)
            self.tview.resizeRowsToContents()
            self.tview.resizeColumnsToContents()

    def increase(self):
        if self.cols < 5:
            self.cols = self.cols + 1
            self.model.setCols(self.cols)
            mw, mh = self.width(), self.height()
            self.delegate.setParas(mw, self.cols)
            self.tview.resizeRowsToContents()
            self.tview.resizeColumnsToContents()

    def resizeEvent(self, event):
        mw, mh = event.size().width(), event.size().height()
        self.delegate.setParas(mw, self.cols)
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = ImageWindow(IMAGEFILESPATH)
    window1.show()
    app.exec_()
