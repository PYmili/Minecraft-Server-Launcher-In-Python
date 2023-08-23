"""
调用 MISLIP_lib 中的MainWindow类并显示。
"""
import sys

from loguru import logger
from PyQt5.QtWidgets import QApplication
from MSLIP_lib import MainWindow


if __name__ == '__main__':
    logger.add(r"./log/latest.log", rotation="10kb")
    app = QApplication(sys.argv)
    logger.info("正常启动程序")
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())