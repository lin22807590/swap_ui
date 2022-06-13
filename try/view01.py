import glob
import math
import sys
from collections import namedtuple

from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate

# Create a custom namedtuple class to hold our data.
preview = namedtuple("preview", "id title image")

NUMBER_OF_COLUMNS = 4
CELL_PADDING = 10 # all sides

class PreviewDelegate(QStyledItemDelegate):
    
    def getImage(self, option, index):
        # data is our preview object
        data = index.model().data(index, Qt.DisplayRole)
        if data is None:
            return
        return data.image

    def paint(self, painter, option, index):

        dataImg = self.getImage(option, index)
        if dataImg is None:
            return

        width = option.rect.width() - CELL_PADDING * 2
        height = option.rect.height() - CELL_PADDING * 2

        # option.rect holds the area we are painting on the widget (our table cell)
        # scale our pixmap to fit
        scaled = dataImg.scaled(
            width,
            height,
            aspectRatioMode=Qt.KeepAspectRatio,
        )
        # Position in the middle of the area.
        x = CELL_PADDING + (width - scaled.width()) / 2
        y = CELL_PADDING + (height - scaled.height()) / 2
        
        painter.drawImage(round(option.rect.x() + x), round(option.rect.y() + y), scaled)
        
    def sizeHint(self, option, index):
        # All items the same size.
        dataImg = self.getImage(option, index)
        if not dataImg is None:
            size = dataImg.size()
            dwidth = 300
            h = round(dwidth*size.height()/size.width())
            return QSize(dwidth, h)
        return QSize(300, 168)


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
            return data.title

    def columnCount(self, index):
        return self.cols

    def rowCount(self, index):
        n_items = len(self.previews)
        return math.ceil(n_items / self.cols)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = QTableView()
        self.view.horizontalHeader().hide()
        self.view.verticalHeader().hide()
        self.view.setGridStyle(Qt.NoPen)
        
        delegate = PreviewDelegate()
        self.view.setItemDelegate(delegate)
        self.model = PreviewModel()
        self.view.setModel(self.model)
        
        self.setCentralWidget(self.view)

        # Add a bunch of images.
        for n, fn in enumerate(glob.glob("imgs/*.jpg")):
            image = QImage(fn)
            item = preview(n, fn, image)
            self.model.previews.append(item)
        self.model.layoutChanged.emit()
        
        self.view.resizeRowsToContents()
        self.view.resizeColumnsToContents()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
