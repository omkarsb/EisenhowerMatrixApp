import sys
from PyQt5.QtWidgets import QApplication
from EisenhowerMatrixApp import EisenhowerMatrixApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EisenhowerMatrixApp()
    sys.exit(app.exec_())
