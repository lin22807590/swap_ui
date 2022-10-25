import glob
import math
import os
import re
import sys
from collections import namedtuple

from PyQt5 import uic, QtCore  # , QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtWidgets import QVBoxLayout
# Create a custom namedtuple class to hold our data.
preview = namedtuple("preview", "id title image")

IMAGEFILESPATH = "/home/mdisk/FaceProj/images/Wash/Wash-boy"
#IMAGEFILESPATH = "imgs"
CELL_PADDING = 2  # all sides


class PreviewDelegate(QStyledItemDelegate):

    def __init__(self, height, cols):
        super().__init__()
        # .data holds our data for display, as a list of Preview objects.
        self.height = height
        self.cols = cols
        self.selections = []

    def setParas(self, height, cols):
        self.height = height
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
        scaled = dataImg.scaled(
            width, height, aspectRatioMode=Qt.KeepAspectRatio)
        # Position in the middle of the area.
        x = CELL_PADDING + (width - scaled.width()) / 2
        y = CELL_PADDING + (height - scaled.height()) / 2

        painter.drawImage(int(option.rect.x() + x),
                          int(option.rect.y() + y), scaled)

    def sizeHint(self, option, index):
        # All items the same size.
        data = index.model().data(index, Qt.DisplayRole)
        if data is None:
            return QSize(0, 0)
        dataImg = data.image
        # w*dataImg.height()/dataImg.width())
        h = max(80, int(0.95*(self.height-120)))
        # max(240, int(0.95*self.width/self.cols))
        w = h*dataImg.width()/dataImg.height()
        return QSize(w, h)


class PreviewModel(QAbstractTableModel):
    def __init__(self, cols=100):
        super().__init__()
        # .data holds our data for display, as a list of Preview objects.
        self.previews = []
        self.cols = cols

    def setCols(self, cols):
        self.cols = cols
        self.layoutChanged.emit()

    def data(self, index, role):
        try:
            data = self.previews[index.row() * self.cols + index.column()]
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
        return 1
        # n_items = len(self.previews)
        # return math.ceil(n_items / self.cols)


class ImageWindow(QMainWindow):
    def __init__(self, parent, folder, kind):
        super().__init__()
        self.up = parent
        self.folder = folder
        uic.loadUi('imgWindow.ui', self)  # Load the .ui file
        self.setWindowTitle(self.folder)
        self.cols = 30
        self.tview = QTableView()
        self.tview.horizontalHeader().hide()
        self.tview.verticalHeader().hide()
        self.tview.setGridStyle(Qt.NoPen)
        self.infoSize = "0x0"

        mw, mh = self.width(), self.height()
        self.delegate = PreviewDelegate(mh, self.cols)
        self.tview.setItemDelegate(self.delegate)
        self.model = PreviewModel()
        self.tview.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.tview)
        self.uwidget.setLayout(layout)

        # Connection
        # self.bdec.clicked.connect(self.decrease)
        # self.binc.clicked.connect(self.increase)
        # self.bOffset.clicked.connect(self.setOffset)
        # self.imgOffset.valueChanged.connect(self.offsetChanged)
        # self.imgOffset.sliderReleased.connect(self.offsetReleased)
        self.bMarkA.clicked.connect(self.setMarkA)
        self.bMarkB.clicked.connect(self.setMarkB)
        self.bInterpolate.clicked.connect(self.interpolation)
        self.tview.clicked.connect(self.imgClicked)
        self.loadFiles()

        # Variation
        self.kind = kind
        if kind == 1:  # Src
            self.bSrcFile.clicked.connect(self.setSrcFile)
        if kind == 2:  # Drive
            self.bSrcFile.hide()
        if kind == 3:
            self.bSrcFile.hide()

    def interpolation(self):
        if hasattr(self, 'markA') and hasattr(self, 'markA'):
            numa, numb = 0, 0
            restr = f".*?(\d+).*"
            ss = re.match(restr, os.path.basename(self.markA))
            if ss:
                numa = int(ss.group(1))
            ss = re.match(restr, os.path.basename(self.markB))
            if ss:
                numb = int(ss.group(1))
            if numa > 0 and numb > 0:
                if self.bInterNum.text() != '' and self.bInterNum.text() != '0':
                    numb = numa + int(self.bInterNum.text())
                cmdstr = f"../../FaceTool/fpInterpolationVlc.py -a {self.markA} -b {self.markB}"
                cmdstr += f" -s {numa} -e {numb}"
                cmdstr += f" -o ./tempinter"
                try:
                    os.system(cmdstr)
                except:
                    pass

    def setMarkA(self):
        if hasattr(self, 'clickFile'):
            self.markA = self.clickFile
            markFile = os.path.basename(self.clickFile)
            self.infoMarkA = f"A={markFile}"
            infoMsg = [self.infoSize, self.infoMarkA]
            if hasattr(self, "infoMarkB"):
                infoMsg.append(self.infoMarkB)
            self.info.setText("   ".join(infoMsg))
            if self.kind == 2:
                self.up.markA = markFile
                self.up.tMarkA.setText(f"MarkA = {markFile}")

    def setMarkB(self):
        if hasattr(self, 'clickFile'):
            self.markB = self.clickFile
            markFile = os.path.basename(self.clickFile)
            self.infoMarkB = f"B={markFile}"
            infoMsg = [self.infoSize]
            if hasattr(self, "infoMarkA"):
                infoMsg.append(self.infoMarkA)
            infoMsg.append(self.infoMarkB)
            self.info.setText("   ".join(infoMsg))
            if self.kind == 2:
                self.up.markB = markFile
                self.up.tMarkB.setText(f"MarkB = {markFile}")

    def setSrcFile(self):
        if hasattr(self, 'clickFile'):
            self.up.srcFile = self.clickFile
            self.up.tSrcFile.setText(self.clickFile)

    def imgClicked(self, index):
        offset = index.row() * self.cols + index.column()
        data = self.model.previews[offset]
        self.clickFile = data.title
        # if offset < len(self.model.previews):
        #     self.clickPos = self.imgOffset.value() + offset
        #     sizeText = f"Image Size: ({data.image.width()}, {data.image.height()})"
        #     posText = f"Clicked: {self.clickPos}"
        #     self.info.setText(sizeText+"  "+posText)

    def loadFiles(self):
        types = ('*.png', '*.jpg')  # the tuple of file types
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(f"{self.folder}/{files}"))
        self.files = files_grabbed
        self.files.sort()
        self.loadImages(0)
        self.show()  # Show the GUI
        self.uwidget.update()

    def offsetChanged(self, value):
        self.imgSRLabel.setText(f"Offset: {value:04d}")

    def loadImages(self, offset):
        # rightidx = min(len(self.files), offset+DEFAULT_LOAD_MAX_PICS-1)
        # Add a bunch of images.
        self.model.previews = []
        for n, fn in enumerate(self.files):  # [offset:rightidx]):
            image = QImage(fn)
            if n == 0:
                self.infoSize = f"Image:{image.width()}x{image.height()}"
                self.info.setText(self.infoSize)
            item = preview(n, fn, image)
            self.model.previews.append(item)
        self.cols = len(self.files)
        mw, mh = self.width(), self.height()
        self.delegate.setParas(mh, self.cols)
        self.model.setCols(self.cols)
        self.model.layoutChanged.emit()
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()

    def decrease(self):
        if self.cols > 1:
            self.cols = self.cols - 1
            self.model.setCols(self.cols)
            mw, mh = self.width(), self.height()
            self.delegate.setParas(mh, self.cols)
            self.tview.resizeRowsToContents()
            self.tview.resizeColumnsToContents()

    def increase(self):
        if self.cols < 5:
            self.cols = self.cols + 1
            self.model.setCols(self.cols)
            mw, mh = self.width(), self.height()
            self.delegate.setParas(mh, self.cols)
            self.tview.resizeRowsToContents()
            self.tview.resizeColumnsToContents()

    def resizeEvent(self, event):
        mw, mh = event.size().width(), event.size().height()
        self.delegate.setParas(mh, self.cols)
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = ImageWindow(None, IMAGEFILESPATH, 3)
    window1.show()
    app.exec_()
