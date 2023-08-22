"""
调用 MISLIP_lib 中的MainWindow类并显示。
"""
import sys
from PyQt5.QtWidgets import QApplication
from MSLIP_lib import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())