import requests
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QListWidgetItem,
)
from fake_user_agent import user_agent
from lxml import etree

from .BackendMethods import BackendMethod


class VersionListThread(QThread):
    """版本加载线程"""

    def __init__(self):
        super().__init__()
        self.version_lists = []
        self.hand = {'User-Agent': user_agent()}
        self.server_list_url = 'https://getbukkit.org/download/spigot'

    def run(self):
        req = requests.get(url=self.server_list_url, headers=self.hand)
        html = etree.HTML(req.text)
        self.version_list = html.xpath('//div[@class="download-pane"]/div//div[1]/h2/text()')
        self.version_lists = self.version_list

    def return_list(self):
        return self.version_lists


class DownloadOfficial(QThread):
    """官方server下载线程"""

    def __init__(self, download_btn: QPushButton):
        super().__init__()
        self.download_btn = download_btn

    def run(self) -> None:
        back_method = BackendMethod(select_v=self.download_btn.text())
        back_method.DownloadJar_official()


class DownloadSpigot(QThread):
    """spigot server下载线程"""

    def __init__(self, download_btn: QPushButton):
        super().__init__()
        self.download_btn = download_btn

    def run(self) -> None:
        back_method = BackendMethod(select_v=self.download_btn.text())
        back_method.DownloadJar_spigot()


class DownloadWindow(QWidget):
    """窗体，线程调用，功能类"""

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        # 创建左侧按钮选择区
        self.left_button_layout = QVBoxLayout()

        self.button_official = QPushButton("官方内核")
        self.button_spigot = QPushButton("Sipgot")
        self.button_forge = QPushButton("Forge")

        self.button_official.clicked.connect(self.add_official_to_list)
        self.button_spigot.clicked.connect(self.add_spigot_to_list)
        self.button_forge.clicked.connect(self.add_forge_to_list)

        self.button_official.setStyleSheet(
            "QPushButton {"
            "background-color: #b0d4ff;"
            "border: 1px solid #ccc;"
            "padding: 8px;"
            "border-radius: 10px;"  # 设置圆角
            "}"
            "QPushButton:hover {"
            "background-color: #a0c4ff;"
            "}"
        )

        self.button_spigot.setStyleSheet(
            "QPushButton {"
            "background-color: #ffccb0;"
            "border: 1px solid #ccc;"
            "padding: 8px;"
            "border-radius: 10px;"  # 设置圆角
            "}"
            "QPushButton:hover {"
            "background-color: #ffbb9f;"
            "}"
        )

        self.button_forge.setStyleSheet(
            "QPushButton {"
            "background-color: #b0ffb0;"
            "border: 1px solid #ccc;"
            "padding: 8px;"
            "border-radius: 10px;"  # 设置圆角
            "}"
            "QPushButton:hover {"
            "background-color: #a0ffa0;"
            "}"
        )

        self.left_button_layout.addWidget(self.button_official)
        self.left_button_layout.addWidget(self.button_spigot)
        self.left_button_layout.addWidget(self.button_forge)

        # 创建右侧列表信息显示区
        self.right_list_layout = QVBoxLayout()
        self.info_list = QListWidget()
        self.right_list_layout.addWidget(self.info_list)

        self.info_list.setStyleSheet(
            "QListWidget {"
            "background-color: rgba(240, 240, 240, 150);"
            "border: 1px solid #ccc;"
            "}"
            "QListWidget::item {"
            "background-color: white;"
            "border: none;"  # 去掉按钮边框
            "padding: 5px;"
            "}"
            "QListWidget::item:selected {"
            "background-color: #b0d4ff;"
            "color: black;"
            "}"
            "QListWidget::item:hover {"
            "background-color: #e0e0e0;"
            "}"
        )
        # 将左侧按钮选择区和右侧列表信息显示区添加到主布局中
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_button_layout)
        self.main_layout.addLayout(self.right_list_layout)

        self.setLayout(self.main_layout)

    def add_button_to_list(self, button_text):
        button = QPushButton(button_text)
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #b0d4ff;"
            "border: none;"  # 去掉按钮边框
            "border-radius: 10px;"  # 圆角
            "color: black;"
            "}"
            "QPushButton:hover {"
            "background-color: #a0c4ff;"
            "}"
        )

        item = QListWidgetItem()
        self.info_list.addItem(item)
        self.info_list.setItemWidget(item, button)

    def add_official_to_list(self):
        self.info_list.clear()
        self.add_button_to_list("官方内核")

    def add_spigot_to_list(self):
        self.info_list.clear()
        self.add_button_to_list("Sipgot")

    def add_forge_to_list(self):
        self.info_list.clear()
        self.add_button_to_list("Forge")