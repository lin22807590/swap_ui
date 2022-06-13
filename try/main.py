import sys, re, os
from PyQt5 import uic #, QtWidgets 
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QMessageBox, QStatusBar
from imgWindow import ImageWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self) # Load the .ui file
        self.setWindowTitle("Head Swap")
        self.bSrcFolder.clicked.connect(self.openSrcFolder)
        self.bDriveFolder.clicked.connect(self.openDriveFolder)
        self.bSetSource.clicked.connect(self.setSourceFile)
        self.bSetDriveA.clicked.connect(self.setDriveMarkA)
        self.bSetDriveB.clicked.connect(self.setDriveMarkB)
        self.bRunFirst.clicked.connect(self.runFirst)
        self.bQuit.clicked.connect(lambda: quit())
        self.src = None
        self.drive = None
        self.result = None

    def runFirst(self):
        cmdstr = f"fpFirstOrderDir.py --source_image {self.srcFile}"
        cmdstr += f" --driving_dir {self.driveFolder}"
        cmdstr += f" --output_dir ./tempoutput"
        if self.cRelative.isChecked():
            cmdstr += " --relative"

        if self.cFindBest.isChecked():
            cmdstr += f" --find_best_frame"

        restr = f".*?(\d+).*"
        ss = re.match(restr, self.markA)
        if ss:
            cmdstr += f" --start {ss.group(1)}"
        ss = re.match(restr, self.markB)
        if ss:
            cmdstr += f" --end {ss.group(1)}"
        os.system(cmdstr)
        if self.result:
            self.result.close()
        self.result = ImageWindow(self, "./tempoutput", 3)
        self.result.show()


    def setDriveMarkA(self):
        if self.drive and self.drive.clickFile:
            markFile = os.path.basename(self.drive.clickFile)
            self.markA = markFile
            self.tMarkA.setText(f"MarkA = {markFile}")

    def setDriveMarkB(self):
        if self.drive and self.drive.clickFile:
            markFile = os.path.basename(self.drive.clickFile)
            self.markB = markFile
            self.tMarkB.setText(f"MarkB = {markFile}")

    def setSourceFile(self):
        if self.src and self.src.clickFile:
            self.srcFile = self.src.clickFile
            self.tSrcFile.setText(f"Source File = {self.srcFile}")

    def openSrcFolder(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory",
            ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir is None or dir == "":
            return
        if self.src:
            self.src.close()
        self.srcFolder = dir
        self.tSrcFolder.setText(f"Source Folder = {dir}")
        self.src = ImageWindow(self, self.srcFolder, 1)
        self.src.show()

    def openDriveFolder(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory",
            ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir is None or dir == "":
            return
        if self.drive:
            self.drive.close()
        self.driveFolder = dir
        self.tDriveFolder.setText(f"Driving Folder = {dir}")
        self.drive = ImageWindow(self, self.driveFolder, 2)
        self.drive.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()
