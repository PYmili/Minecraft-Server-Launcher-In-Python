import os
import json

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QGroupBox,
    QDialog,
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# 添加服务器界面
from .IncreaseServer import AddButtonWindow
from .DeleteServerWindow import DeleteServerWindow


class CreateWindow(QWidget):
    """创建服务器界面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_button_window = None
        self.AddButton = QPushButton("添加", self)
        self.DeleteServerButton = QPushButton("删除", self)
        self.gridLayout = QGridLayout()  # 使用 QGridLayout 作为网格布局
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # 设置添加按钮样式
        self.AddButton.setFont(QFont("Arial", 14, QFont.Bold))
        self.AddButton.setStyleSheet(
            "QPushButton { background-color: green; color: white; border: none; padding: 10px 20px; }"
            "QPushButton:hover { background-color: darkgreen; }"
            "QPushButton:pressed { background-color: lightgreen; }"
        )
        self.AddButton.setCursor(Qt.PointingHandCursor)
        self.AddButton.clicked.connect(self.addButtonShow)  # 连接添加按钮的点击事件

        # 删除服务器
        self.DeleteServerButton.setFont(QFont("Arial", 14, QFont.Bold))
        self.DeleteServerButton.setStyleSheet(
            "QPushButton { background-color: red; color: white; border: none; padding: 10px 20px; }"
            "QPushButton:hover { background-color: darkred; }"
            "QPushButton:pressed { background-color: lightred; }"
        )
        self.DeleteServerButton.setCursor(Qt.PointingHandCursor)
        self.DeleteServerButton.clicked.connect(self.ShowDeleteServerWindow)

        # 创建一个 QGroupBox 来包含按钮布局
        button_group = QGroupBox()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.AddButton, alignment=Qt.AlignRight | Qt.AlignBottom)
        button_layout.addWidget(self.DeleteServerButton, alignment=Qt.AlignRight | Qt.AlignBottom)
        button_group.setLayout(button_layout)
        button_group.setStyleSheet("QGroupBox { border: none; }")

        # 添加网格布局到主垂直布局
        main_layout.addLayout(self.gridLayout)

        # 添加按钮组到主垂直布局
        main_layout.addWidget(button_group)

        self.setLayout(main_layout)

        self.UpdateCard()

    # 显示添加服务器配置界面
    def addButtonShow(self) -> None:
        self.add_button_window = AddButtonWindow()
        result = self.add_button_window.exec_()
        if result == QDialog.Accepted:
            self.UpdateCard()

    def ShowDeleteServerWindow(self) -> None:
        self.DeleteServer = DeleteServerWindow()
        result = self.DeleteServer.exec_()
        if result == QDialog.Accepted:
            self.UpdateCard()

    # 更新卡片
    def UpdateCard(self) -> None:
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        with open("./Servers/Servers.json", "r", encoding="utf-8") as rfp:
            ServerData = json.loads(rfp.read())

        for i in ServerData.keys():
            self.addCard(
                ServerData[i]['ServerName'] +
                "\n使用框架：" +
                os.path.split(ServerData[i]['framework'])[-1] +
                "\n创建时间：" +
                ServerData[i]['CreationTime']
            )

    # 添加一个卡片用于显示当前已创建的服务器列表
    def addCard(self, text: str):
        card_button = QPushButton(text, self)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        card_button.setFont(font)
        card_button.setStyleSheet(
            "QPushButton { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #3399FF, stop: 1 #0066CC);"
            "border-radius: 5px; padding: 10px; color: white; }"
            "QPushButton:hover { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #55aaff, stop: 1 #3399FF); }"
            "QPushButton:pressed { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #0066CC, stop: 1 #004499); }"
        )

        self.gridLayout.addWidget(card_button)  # 在网格中添加卡片按钮


