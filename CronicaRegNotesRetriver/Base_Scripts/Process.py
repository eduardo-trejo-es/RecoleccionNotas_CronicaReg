from PyQt5.QtCore import *

import  time

class Process(QThread):
    Update_Progress = pyqtSignal(int)
    def __init__(self):
        super().__init__()
    
    def setValues(self,var):
        self.Var=var

    def run(self):
        for i in range(0, 100,self.Var):
            time.sleep(1)
            self.Update_Progress.emit(i)
            