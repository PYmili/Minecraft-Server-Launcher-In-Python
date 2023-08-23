import requests
from PyQt5.QtCore import QThread
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
        self.server_version_lists = []
        self.forge_version_list = []
        self.hand = {'User-Agent': user_agent()}
        self.server_list_url = 'https://getbukkit.org/download/spigot'
        self.forge_list_url = 'https://files.minecraftforge.net/net/minecraftforge/forge'

    def run(self):
        req = requests.get(url=self.server_list_url, headers=self.hand)
        html = etree.HTML(req.text)
        version_list = html.xpath('//div[@class="download-pane"]/div//div[1]/h2/text()')
        self.server_version_lists = version_list
        self.run_()

    def run_(self):
        req = requests.get(url=self.forge_list_url, headers=self.hand)
        html = etree.HTML(req.text)
        version_list = html.xpath('//li[@class="li-version-list"]/ul//li//text()')
        self.forge_version_list = [i.strip() for i in version_list if i.strip() != '']

    def return_list(self):
        return self.server_version_lists, self.forge_version_list


class DownloadOfficial(QThread):
    """官方server下载线程"""

    def __init__(self, download_btn: QPushButton):
        super().__init__()
        self.download_btn = download_btn

    def run(self) -> None:
        back_method = BackendMethod(select_v=self.download_btn.text())
        back_method.Download_official()


class DownloadSpigot(QThread):
    """spigot server下载线程"""

    def __init__(self, download_btn: QPushButton):
        super().__init__()
        self.download_btn = download_btn

    def run(self) -> None:
        back_method = BackendMethod(select_v=self.download_btn.text())
        back_method.Download_spigot()


class DownloadForge(QThread):
    """spigot server下载线程"""

    def __init__(self, download_btn: QPushButton):
        super().__init__()
        self.download_btn = download_btn

    def run(self) -> None:
        back_method = BackendMethod(select_v=self.download_btn.text())
        back_method.Download_forge()


class DownloadWindow(QWidget):
    """窗体，线程调用，功能类"""

    def __init__(self):
        super().__init__()
        self.load_list_thread = VersionListThread()
        self.load_list_thread.start()
        self.load_list_thread.finished.connect(self.add_official_to_list)
        self.load_list_thread.finished.connect(self.add_spigot_to_list)
        self.load_list_thread.finished.connect(self.add_forge_to_list)

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

    def add_button_to_list(self, button_text, event_fun):
        button = QPushButton(button_text)
        if event_fun != '':
            button.clicked.connect(lambda: event_fun(button))
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

    def add_official_to_list(self) -> None:
        """官方server下载列表"""
        self.info_list.clear()
        self.add_button_to_list("官方内核", '')
        self.version_list = self.load_list_thread.return_list()[0]
        for version in self.version_list:
            self.add_button_to_list(f'{version}', event_fun=self.download_official)

    def add_spigot_to_list(self) -> None:
        self.info_list.clear()
        self.add_button_to_list("Sipgot", '')
        self.version_list = self.load_list_thread.return_list()[0]
        for version in self.version_list:
            self.add_button_to_list(f'{version}', event_fun=self.download_spigot)

    def add_forge_to_list(self) -> None:
        self.info_list.clear()
        self.add_button_to_list("Forge", '')
        self.version_list = self.load_list_thread.return_list()[1]
        for version in self.version_list:
            self.add_button_to_list(f'{version}', event_fun=self.download_forge)

    def download_official(self, download_btn: QPushButton):
        """DownloadOfficial线程调用"""
        self.download_official_thread = DownloadOfficial(download_btn=download_btn)
        self.download_official_thread.start()

    def download_spigot(self, download_btn: QPushButton):
        """DownloadSpigot线程调用"""
        self.download_spigot_thread = DownloadSpigot(download_btn=download_btn)
        self.download_spigot_thread.start()

    def download_forge(self, download_btn: QPushButton):
        """DownLoadForge线程调用"""
        self.download_forge_thread = DownloadForge(download_btn=download_btn)
        self.download_forge_thread.start()
