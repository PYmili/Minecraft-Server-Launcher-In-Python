import json
import shutil
import os

from PyQt5.QtWidgets import (
    QDesktopWidget,
    QComboBox,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
)


class DeleteServerWindow(QDialog):
    """删除服务器界面"""

    def __init__(self):
        super(DeleteServerWindow, self).__init__(parent=None)

        # 用于判断程序是否成功写入ServerToRun.json
        self.IfWrite = False

        self.setWindowTitle("服务器选择")
        self.setGeometry(100, 100, 300, 150)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

        layout = QVBoxLayout()

        self.server_combo_box = QComboBox(self)
        self.getServerList()
        layout.addWidget(self.server_combo_box)

        button_layout = QHBoxLayout()

        confirm_button = QPushButton("确认", self)
        confirm_button.clicked.connect(self.DeleteServers)
        button_layout.addWidget(confirm_button)

        cancel_button = QPushButton("取消", self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def getServerList(self) -> dict:
        result = {}
        with open("./Servers/Servers.json", "r", encoding="utf-8") as rfp:
            result = json.loads(rfp.read())
            for key, value in result.items():
                self.server_combo_box.addItem(key)  # 添加服务器选项

        return result

    def DeleteServers(self):
        key = self.server_combo_box.currentText()
        if key:
            self.__DeleteServerThread = DeleteServerThread(key)
            self.__DeleteServerThread.result_ready.connect(self.AcceptDeleteServerThread)
            self.__DeleteServerThread.start()

    def AcceptDeleteServerThread(self, result):
        QMessageBox.information(
            self, "结果", result,
            QMessageBox.Yes
        )
        if result == "删除成功！":
            self.accept()
            self.close()
        self.close()


class DeleteServerThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, ServerName):
        super(DeleteServerThread, self).__init__(parent=None)
        self.ServerName = ServerName

    def run(self):
        try:
            rfp = open("./Servers/Servers.json", "r", encoding="utf-8")
            data = json.loads(rfp.read())
            rfp.close()

            shutil.rmtree(
                os.path.split(data[self.ServerName]['framework'])[0]
            )

            del data[self.ServerName]
            with open("./Servers/Servers.json", "w+", encoding="utf-8") as wfp:
                wfp.write(json.dumps(data))

            self.result_ready.emit("删除成功！")
        except Exception as e:
            self.result_ready.emit(e)
