import requests
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy
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


class JarDownLoad(QWidget):
    """窗体，线程调用，功能类"""

    def __init__(self):
        super().__init__()
        self.load_list_thread = VersionListThread()
        self.load_list_thread.start()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.group_official = QGroupBox('官方版本', self)
        self.group_official.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.official_lay = QVBoxLayout()
        self.load_list_thread.finished.connect(lambda:
                                               self.official_list(layout=self.official_lay))
        self.group_official.setLayout(self.official_lay)

        self.group_spigot = QGroupBox('spigot版本', self)
        self.group_spigot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spigot_lay = QVBoxLayout()
        self.load_list_thread.finished.connect(lambda:
                                               self.spigot_list(layout=self.spigot_lay))

        self.group_spigot.setLayout(self.spigot_lay)

        self.jar_window = QHBoxLayout(self)
        self.jar_window.setAlignment(Qt.AlignTop)
        self.jar_window.addWidget(self.group_official)
        self.jar_window.addWidget(self.group_spigot)

        widget = QWidget(self)
        widget.setLayout(self.jar_window)
        self.scroll_area.setWidget(widget)

        self.main_window = QVBoxLayout()
        self.main_window.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.main_window.addWidget(self.scroll_area)
        self.setLayout(self.main_window)

    def official_list(self, layout: QVBoxLayout):
        """官方server下载列表"""
        self.version_list = self.load_list_thread.return_list()
        for version in self.version_list:
            self.load_official(version=version, layout=layout)

    def spigot_list(self, layout: QVBoxLayout):
        """spigot下载列表"""
        self.version_list = self.load_list_thread.return_list()
        for version in self.version_list:
            self.load_spigot(version=version, layout=layout)

    def load_official(self, version: str, layout: QVBoxLayout):
        download_btn = QPushButton(f'{version}', self)
        download_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        download_btn.clicked.connect(lambda: self.download_official(download_btn=download_btn))
        layout.addWidget(download_btn)

    def load_spigot(self, version: str, layout: QVBoxLayout):
        download_btn = QPushButton(f'{version}', self)
        download_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #
        download_btn.clicked.connect(lambda: self.download_spigot(download_btn=download_btn))
        layout.addWidget(download_btn)

    def download_official(self, download_btn: QPushButton):
        """DownloadOfficial线程调用"""
        self.download_official_thread = DownloadOfficial(download_btn=download_btn)
        self.download_official_thread.start()

    def download_spigot(self, download_btn: QPushButton):
        """DownloadSpigot线程调用"""
        self.download_spigot_thread = DownloadSpigot(download_btn=download_btn)
        self.download_spigot_thread.start()
