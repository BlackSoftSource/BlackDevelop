from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from ui import MainWindow

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication(sys.argv)
ui = Main()
ui.show()
sys.exit(app.exec_())
