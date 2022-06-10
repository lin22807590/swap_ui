from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap
import os
import cv2

class output_order(object):
    def __init__(self, input, driving_video, output, start, end ):
        
        self.input=input
        self.driving_video=driving_video
        self.output=output
        self.start=start
        self.end=end
        self.createbatfile()
        print(f'-i {self.input} -d {self.driving_video}-o {self.output} -s {start} -e{end} ' )
        os.system(".\\execute.bat")


    def createbatfile(self):
        with open(r'execute.bat','a+',encoding='utf-8')as test:
            test.truncate(0)    
        f=open("execute.bat", "a")
        f.write('@echo OFF')
        f.write('\n')
        f.write('set CONDAPATH=C:\\Users\\user\\Anaconda3')
        f.write('\n')
        f.write('set ENVNAME=motion')
        f.write('\n')
        f.write('if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\\envs\\%ENVNAME%)')
        f.write('\n')
        f.write('call %CONDAPATH%\Scripts\\activate.bat %ENVPATH%')
        f.write('\n')
        f.write('python d:\\program\\first-order-model\\demodir.py ')
        f.write('--config d:\\program\\first-order-model\\config\\vox-256.yaml ')
        f.write('--checkpoint d:\\program\\first-order-model\\vox-cpk.pth.tar ')
        f.write(f'--source_image {self.input} ')
        f.write(f'--driving_dir {self.driving_video} ')
        #f.write('--driving_dir d:\\program\\first-order-model\\pics\\focus03\\ ')
        f.write(f'--relative --output_dir {self.output}\\ ')
        f.write(f'--find_best_frame ')
        f.write(f'--start {self.start} ')
        f.write(f'--end {self.end}')
        f.write('\n')
        f.write('call conda deactivate')
        f.write('\n')
        f.write('timeout /t 5')
        f.write('\n')
        f.close()

