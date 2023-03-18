import os, glob, re
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize, QModelIndex
from collections import namedtuple
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QDialog, QMessageBox

# Create a custom namedtuple class to hold our data.
timage = namedtuple("timage", "id title image")

CELL_PADDING = 2  # all sides

class FR_Delegate(QStyledItemDelegate):

    def __init__(self, size):
        super().__init__()
        self.size = size
        self.cols = 1
        self.selections = []

    def setSize(self, size): #, cols):
        self.size = size
        # self.cols = cols

    def getImage(self, index):
        data = index.model().data(index, Qt.DisplayRole)
        if data is None:
            if index.row(): # Source
                return timage(1, 'source', QImage('source.png'))
        return data

    def paint(self, painter, option, index):
        data = self.getImage(index)
        if data is None: return
        dataImg = data.image
        width = option.rect.width() - CELL_PADDING * 2
        height = option.rect.height() - CELL_PADDING * 2
        scaled = dataImg.scaled(width, height,
                aspectRatioMode=Qt.KeepAspectRatio)
        x = CELL_PADDING + (width - scaled.width()) / 2
        y = CELL_PADDING + (height - scaled.height()) / 2
        painter.drawImage(int(option.rect.x() + x),
                          int(option.rect.y() + y), scaled)

    def sizeHint(self, option, index):
        data = self.getImage(index)
        if data is None: return QSize(0, 0)
        dataImg = data.image
        w, h = self.size.width(), self.size.height()
        h = (h-CELL_PADDING*2)/2
        w = h*dataImg.width()/dataImg.height()
        return QSize(w, h)
        # w*dataImg.height()/dataImg.width())
        # max(240, int(0.95*self.width/self.cols))


class FR_Model(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        itemD = timage(0, 'drive', QImage('drive.png'))
        # itemS = timage(1, 'source', QImage('source.png'))
        self.drives = [itemD]
        self.sources = [None]

    def data(self, index, role):
        if index.row(): data = self.sources[index.column()]
        else: data = self.drives[index.column()]
        if role == Qt.DisplayRole: return data
        if role == Qt.ToolTipRole:
            if data: return os.path.basename(data.title)
            return ""

    def columnCount(self, index):
        return len(self.drives)

    def rowCount(self, index):
        return 2

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal: return section+1
            if orientation == Qt.Vertical:
                if section: return 'S'
                else: return 'D'

    def setData(self, index, value, role):
        if role == Qt.EditRole and index.row()==1:
            self.sources[index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False

class FR_TableView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.doubleClicked.connect(self.imgDblClicked)


    def imgDblClicked(self, index):
        if index.row()==0: # Drive
            dir = QFileDialog.getExistingDirectory(self, "Open Directory",
                ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if dir is None or dir == "": return
            types = ('*.png', '*.jpg')  # the tuple of file types
            files_grabbed = []
            for files in types:
                files_grabbed.extend(glob.glob(f"{dir}/{files}"))
            self.drvDir = dir
            files = files_grabbed
            files.sort()

            newdrives = []
            for n, fn in enumerate(files):  # [offset:rightidx]):
                image = QImage(fn)
                # if n == 0:
                #     self.infoSize = f"Image:{image.width()}x{image.height()}"
                #     self.info.setText(self.infoSize)
                item = timage(n, fn, image)
                newdrives.append(item)

            flen = len(newdrives)
            self.model().drives = newdrives
            self.model().sources = self.model().sources[:flen] + \
                [None]*(flen - len(self.model().sources))
            self.model().layoutChanged.emit()
            self.resizeRowsToContents()
            self.resizeColumnsToContents()
        else: # Source
            filename, _ = QFileDialog.getOpenFileName(self, 
                "Open file", ".", 'Image files (*.jpg *.gif *.png *.jpeg)') # start path
            if filename == "": return
            image = QImage(filename)
            col = index.column()
            item = timage(col, filename, image)
            self.model().setData(index, item, Qt.EditRole)
            self.update()
            
    # def horizontalScrollbarValueChanged(self, value):
    #     data = self.parent.model.previews[value]
    #     self.parent.info.setText(f"{os.path.basename(data.title)}")
    def resizeEvent(self, event):
        self.itemDelegate().setSize(event.size())
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def selectionChanged(self, selected, deselected):
        idxs = selected.indexes()
        if len(idxs) > 0 and idxs[0].row():
            self.selected = idxs[0]

    def keyReleaseEvent(self, k):
        if k.key() == 16777223 and self.selected.row():
            self.model().setData(self.selected, None, Qt.EditRole)
        if k.text() == 'x': quit()
        if k.text() == 'm': self.doMoab()
        if k.text() == 'c':
            if not os.path.exists('./result'):
                os.makedirs('./result')
            os.system('cp output/* result/')
            print("Files copied to result")
        if k.text() == 'o':
            os.system('fpPlaydir.py -i output')
        if k.text() == 'r':
            os.system('fpPlaydir.py -i result')

    def doMoab(self):
        srcs = []
        for src in self.model().sources:
            if src:
                srcs.append(src)
                if len(srcs) == 2: break
        drv1 = self.model().drives[srcs[0].id]
        drv2 = self.model().drives[srcs[1].id]
        m = re.search(r'\d+', os.path.basename(drv1.title))
        start = int(m.group(0))
        m = re.search(r'\d+', os.path.basename(drv2.title))
        end = int(m.group(0))
        cmd = f'fpMoab.py -a {srcs[0].title} -b {srcs[1].title} '
        cmd += f'-d {self.drvDir} -s {start} -e {end}'
        os.system(cmd)
