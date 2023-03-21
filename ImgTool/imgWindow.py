import glob
import math
import os, datetime
import re, shutil
import sys
from collections import namedtuple

from PyQt5 import uic, QtCore  # , QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize, QModelIndex
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QDialog, QMessageBox, QInputDialog
# Create a custom namedtuple class to hold our data.
preview = namedtuple("preview", "id title image")

IMAGEFILESPATH = "/home/mdisk/FaceProj/images/Wash/Wash-boy"
#IMAGEFILESPATH = "imgs"
CELL_PADDING = 2  # all sides

class NewImage(QDialog):
    def __init__(self, parent, filename):
        super(NewImage, self).__init__()
        self.parent = parent
        self.filename = filename
        uic.loadUi('newImage.ui', self)
        self.pixmap = QPixmap(filename)
        self.qimage.setPixmap(self.pixmap)
        self.degree.valueChanged.connect(self.rotateImage)

    def rotateImage(self, v):
        transform = QTransform().rotate(v)
        img = self.pixmap.toImage()
        color = img.pixelColor(8, 8)
        cmean = (color.red()+color.green()+color.blue())/3
        newpixmap = self.pixmap.transformed(transform)
        xoffset = (newpixmap.width() - self.pixmap.width()) // 2
        yoffset = (newpixmap.height() - self.pixmap.height()) // 2
        rotated = newpixmap.copy(xoffset, yoffset, self.pixmap.width(), self.pixmap.height());
        img = QImage(self.pixmap.width(), self.pixmap.height(), QImage.Format_RGB32) #width(), self.pixmap.height()) #
        if cmean > 220:
            img.fill(Qt.white) # Set the red background
        else:
            img.fill(Qt.black)
        painter = QPainter(img)
        painter.drawImage(QtCore.QPoint(0,0), rotated.toImage())
        del painter
        self.img = img
        self.qimage.setPixmap(QPixmap.fromImage(img))

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
        h = max(80, int(0.95*(self.height-150)))
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

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal: return section+1
            if orientation == Qt.Vertical:
                return 'S'
class MyTableView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    def horizontalScrollbarValueChanged(self, value):
        data = self.parent.model.previews[value]
        self.parent.info.setText(f"{os.path.basename(data.title)}")
    def selectionChanged(self, selected, deselected):
        if len(selected) > 0:
            selidxs = selected[0].indexes() #self.selectedIndexes()
            slen = len(selidxs)
            bcol = selidxs[0].column()
            ecol = selidxs[slen-1].column()
            bfile = self.model().previews[bcol].title
            bfile = os.path.basename(bfile)
            efile = self.model().previews[ecol].title
            efile = os.path.basename(efile)
            self.parent.info.setText(f"{bfile}--{efile}")


class ImageWindow(QMainWindow):
    def __init__(self, parent, folder, kind):
        super().__init__()
        self.up = parent
        self.folder = folder
        uic.loadUi('imgWindow.ui', self)  # Load the .ui file
        self.setWindowTitle(self.folder)
        self.cols = 30
        self.tview = MyTableView(self)
        # self.tview.horizontalHeader().hide()
        self.tview.verticalHeader().hide()
        self.tview.setGridStyle(Qt.NoPen)
        self.infoSize = "0x0"
        self.imgbuf = None
        self.ctrl = False

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
        self.bHead.clicked.connect(self.head)
        self.bInterpolate.clicked.connect(self.interpolation)
        self.tview.clicked.connect(self.imgClicked)
        self.bCopy.clicked.connect(self.copy)
        self.action_Delete.triggered.connect(self.deleteImage)
        self.bResize.clicked.connect(self.resizeImage)
        self.bHFlip.clicked.connect(self.hflip)
        self.action_Rotate.triggered.connect(self.rotateImage)
        self.bGPEN.clicked.connect(self.GPEN)
        self.bRembg.clicked.connect(self.rembg)
        self.actionRe_name_Files.triggered.connect(self.renameFiles)
        self.actionReload_Files.triggered.connect(self.loadFiles)
        self.loadFiles()

    def GPEN(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory",
            ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir is None or dir == "":
            return
        os.system(f'../../FaceTool/fpGpenDir.py -i {self.folder} -o {dir}')

    def rotateImage(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            col = selidxs[0].column()
            imgfile = self.model.previews[col].title
            nimgwin = NewImage(self, imgfile)
            if nimgwin.exec_():
                item = preview(col, imgfile, nimgwin.img)
                self.model.previews[col] = item
                nimgwin.img.save(imgfile, imgfile[-3:])
                self.model.layoutChanged.emit()
 
    def resizeImage(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            ratio, ok = QInputDialog.getDouble(self, 'Ratio', 
                'Enter the ratio number',
                value=0.45, min=0.3, max=0.7, decimals=2)
            if not ok: return
            for sidx in selidxs:
                col = sidx.column()
                sfile = self.model.previews[col].title
                nsfile = sfile + '.' + sfile[-3:]
                os.system(f'fpResizeImage.py -i {sfile} -o {nsfile} -r {ratio}')
                os.system(f'mv {nsfile} {sfile}')
                image = QImage(sfile)
                item = preview(col, sfile, image)
                self.model.previews[col] = item
            self.model.layoutChanged.emit()

    def hflip(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            for sidx in selidxs:
                col = sidx.column()
                sfile = self.model.previews[col].title
                nsfile = sfile + '.' + sfile[-3:]
                os.system(f'convert {sfile} -flop {nsfile}')
                os.system(f'mv {nsfile} {sfile}')
                image = QImage(sfile)
                item = preview(col, sfile, image)
                self.model.previews[col] = item
            self.model.layoutChanged.emit()

    def deleteImage(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            for index in range(slen, 0, -1):
                col = selidxs[index-1].column()
                sfile = self.model.previews[col].title
                del self.model.previews[col]
                os.system(f'rm {sfile}')
                self.decrease()
            self.tview.setCurrentIndex(QModelIndex())
        mw, mh = self.width(), self.height()
        self.delegate.setParas(mh, len(self.model.previews))
        self.model.setCols(len(self.model.previews))
        self.model.layoutChanged.emit()
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()

    def renameFiles(self):
        nums, ok = QInputDialog.getInt(self, 'Rename Files', 
            'Start number for image files:', value=1, min=1, max=10000, step=1)
        if not ok: return
        bfname = 'image_'
        mlen = len(self.model.previews)
        for i,item in enumerate(self.model.previews):
            if item.title[-3:] == 'jpg':
                print(f'convert {item.title} {item.title[:-3]}png')
                os.system(f'convert {item.title} {item.title[:-3]}png')
                os.system(f'rm {item.title}')
            shutil.copyfile(f'{item.title[:-3]}png', f'{self.folder}/xxx{bfname}{i+nums:04d}.png')
            os.system(f'rm {item.title[:-3]}png')
        for i in range(nums, nums+mlen):
            shutil.move(f'{self.folder}/xxx{bfname}{i:04d}.png',
                f'{self.folder}/{bfname}{i:04d}.png')
        self.loadFiles()

    def copy(self):
        selidxs = self.tview.selectedIndexes()
        if len(selidxs) > 0:
            dir = QFileDialog.getExistingDirectory(self, "Open Directory",
                ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if dir is None or dir == "":
                return
            for index in self.tview.selectedIndexes():
                idx = index.column()
                tfile = self.model.previews[idx].title
                nfile = os.path.join(dir, os.path.basename(tfile))
                os.system(f"cp {tfile} {nfile}")

    def interpolation(self):
        selidxs = self.tview.selectedIndexes()
        checkValid = True
        if len(selidxs) != 2: checkValid = False
        else:
            idxa, idxb = selidxs[:2]
            if idxa.column() > idxb.column(): idxa, idxb = idxb, idxa
            if idxa.column() + 1 != idxb.column(): checkValid = False
        if not checkValid:
            QMessageBox.information(self, 'Interpolation',
                'Currently interpolation only support two continuous selected frames',
                QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            return
        
        nums, ok = QInputDialog.getInt(self, 'Interpolation', 
            'How many frames to interpolate:',
            value=3, min=1, max=127, step=1)
        if not ok: return
        filea = self.model.previews[idxa.column()].title
        fileb = self.model.previews[idxb.column()].title
        cmdstr = f"fpFILM.py -a {filea} -b {fileb} -n {nums}"
        os.system(cmdstr)

        rhead = int(datetime.datetime.now().timestamp())
        tempdir = 'temp/interpolated_frames'
        rhead = int(datetime.datetime.now().timestamp())
        for i in range(1, nums+1):
            file = f'{tempdir}/frame_{i:03d}.png'
            nfile = f'{self.folder}/{rhead+i}.png'
            os.system(f'cp {file} {nfile}')
            pitem = preview(rhead+i, nfile, QImage(nfile))
            self.model.previews.insert(idxa.column()+i, pitem)
        mw, mh = self.width(), self.height()
        self.delegate.setParas(mh, len(self.model.previews))
        self.model.setCols(len(self.model.previews))
        self.model.layoutChanged.emit()
        self.tview.resizeRowsToContents()
        self.tview.resizeColumnsToContents()

    def rembg(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            for sidx in selidxs:
                col = sidx.column()
                sfile = self.model.previews[col].title
                nsfile = sfile + '.' + sfile[-3:]
                os.system(f'fpRemBg.py {sfile} {nsfile}')
                os.system(f'mv {nsfile} {sfile}')
                image = QImage(sfile)
                item = preview(col, sfile, image)
                self.model.previews[col] = item
            self.model.layoutChanged.emit()

    def head(self):
        selidxs = self.tview.selectedIndexes()
        slen = len(selidxs)
        if slen > 0:
            for sidx in selidxs:
                col = sidx.column()
                sfile = self.model.previews[col].title
                nsfile = sfile + '.' + sfile[-3:]
                os.system(f'fpExtractHead.py -i {sfile} -o {nsfile}')
                os.system(f'mv {nsfile} {sfile}')
                image = QImage(sfile)
                item = preview(col, sfile, image)
                self.model.previews[col] = item
            self.model.layoutChanged.emit()


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
        self.loadImages()
        self.show()  # Show the GUI
        self.uwidget.update()

    def offsetChanged(self, value):
        self.imgSRLabel.setText(f"Offset: {value:04d}")

    def loadImages(self):
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

    def keyPressEvent(self, k):
        if k.key() == 16777249: self.ctrl = True

    def keyReleaseEvent(self, k):
        if self.ctrl and k.key() in [16777234, 16777236]: # left, right
            selidxs = self.tview.selectedIndexes()
            slen = len(selidxs)
            if slen != 1: return
            sidx = selidxs[0]
            col = sidx.column()
            if k.key() == 16777234: # left
                if col == 0: return
                t = self.model.previews[col]
                self.model.previews[col] = self.model.previews[col-1]
                self.model.previews[col-1] = t
                prev_index = self.model.index(0, col-1)
                self.tview.clearSelection()
                self.tview.setCurrentIndex(prev_index)
            elif k.key() == 16777236: # right
                if col == len(self.model.previews)-1: return
                t = self.model.previews[col]
                self.model.previews[col] = self.model.previews[col+1]
                self.model.previews[col+1] = t
                next_index = self.model.index(0, col+1)
                self.tview.clearSelection()
                self.tview.setCurrentIndex(next_index)
            self.model.layoutChanged.emit()
        if k.key() == 16777249: self.ctrl = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = ImageWindow(None, IMAGEFILESPATH, 3)
    window1.show()
    app.exec_()
