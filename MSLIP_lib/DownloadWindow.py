import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
    QDialog,
    QLabel,
    QDesktopWidget
)
from fake_user_agent import user_agent
from lxml import etree
from loguru import logger

from .BackendMethods import BackendMethod


class DownloadWindow(QWidget):
    """窗体，线程调用，功能类"""

    def __init__(self):
        super().__init__()
        self.ThreadResult = []
        self.init_ui()

    def init_ui(self):

        # 创建左侧按钮选择区
        self.left_button_layout = QVBoxLayout()

        self.button_official = QPushButton("官方内核")
        self.button_spigot = QPushButton("Sipgot")
        self.button_forge = QPushButton("Forge")

        self.button_official.clicked.connect(lambda : self.addServerToList(0))
        self.button_spigot.clicked.connect(lambda : self.addServerToList(1))
        self.button_forge.clicked.connect(lambda : self.addServerToList(2))

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
        self.info_list.clicked.connect(self.GetInfoListSelect)
        self.right_list_layout.addWidget(self.info_list)

        # 将左侧按钮选择区和右侧列表信息显示区添加到主布局中
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_button_layout)
        self.main_layout.addLayout(self.right_list_layout)
        self.addServerToList(0)

        self.setLayout(self.main_layout)

    def add_button_to_list(self, button_text):
        self.info_list.addItem(button_text)

    def GetInfoListSelect(self):
        Item = self.info_list.currentItem()
        if Item.text():
            self.IfDownLoad = IfDownLoadWindow(Item.text())
            result = self.IfDownLoad.exec_()
            if result == QDialog.Accepted:
                logger.info(f"成功下载{Item.text()}")
                return
            logger.warning(f"未知原因，下载失败{Item.text()}")

    def addServerToList(self, index: int) -> None:
        self.info_list.clear()

        if index == 0:
            self.GetOfficialVersionThread = GetOfficialVersionThread()
            self.GetOfficialVersionThread.result_ready.connect(self.getVersionThreadResult)
            self.GetOfficialVersionThread.start()

        elif index == 1:
            self.GetSpigotVersionListThread = GetSpigotVersionList()
            self.GetSpigotVersionListThread.result_ready.connect(self.getVersionThreadResult)
            self.GetSpigotVersionListThread.start()

        elif index == 2:
            self.GetForgeVersionListThread = GetForgeVersionList()
            self.GetForgeVersionListThread.result_ready.connect(self.getVersionThreadResult)
            self.GetForgeVersionListThread.start()

    def getVersionThreadResult(self, result: list):
        for version in result:
            self.add_button_to_list(f'{version}')


class IfDownLoadWindow(QDialog):
    """确认是否下载内核及下载进度界面"""
    def __init__(self, version, parent=None):
        super().__init__(parent)
        self.setWindowTitle("确认下载")
        self.setGeometry(100, 100, 300, 150)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        self.version = version
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        message_label = QLabel(f"确定要下载版本 {self.version} 吗？", self)
        layout.addWidget(message_label)

        confirm_button = QPushButton("确认", self)
        confirm_button.clicked.connect(self.confirmDownload)
        layout.addWidget(confirm_button)

        cancel_button = QPushButton("取消", self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def confirmDownload(self):
        source, version = self.version.split("-")
        self.th = DownLoadVersionThread(source, version)
        self.th.result_ready.connect(self.GetThreadResult)
        self.th.start()

    def GetThreadResult(self, result: str):
        QMessageBox.information(
            self, "结果", result,
            QMessageBox.Yes
        )
        if result == "下载成功！":
            self.accept()
            self.close()


class DownLoadVersionThread(QThread):
    """下载指定内核线程"""
    result_ready = pyqtSignal(str)

    def __init__(self, source: str, version: str):
        super(DownLoadVersionThread, self).__init__()
        self.source = source
        self.version = version
        self.backend = BackendMethod(
            server_version=version
        )

    def run(self):
        logger.info("启动内核下载线程")
        if self.source == "官方":
            self.backend.Download_official()
        elif self.source == "spigot":
            self.backend.Download_spigot()
        elif self.source == "forge":
            self.backend.Download_forge()

        logger.info("下载成功！")
        self.result_ready.emit("下载成功！")


class GetOfficialVersionThread(QThread):
    """官方版本获取线程"""
    result_ready = pyqtSignal(list)

    def __init__(self):
        super(GetOfficialVersionThread, self).__init__()

    def run(self):
        self.result_ready.emit(
            ["官方-"+i for i in BackendMethod().GetOfficialGameServerList()]
        )


class GetSpigotVersionList(QThread):
    """获取Spigot的版本列表线程"""
    result_ready = pyqtSignal(list)
    
    def __init__(self):
        super(GetSpigotVersionList, self).__init__()
    
    def run(self):
        with requests.get(
                url='https://getbukkit.org/download/spigot',
                headers={'User-Agent': user_agent()}
        ) as get:
            html = etree.HTML(get.text)
            result = html.xpath('//div[@class="download-pane"]/div//div[1]/h2/text()')
            self.result_ready.emit(
                ["spigot-"+i for i in result]
            )


class GetForgeVersionList(QThread):
    """获取Forge的版本列表线程"""
    result_ready = pyqtSignal(list)

    def __init__(self):
        super(GetForgeVersionList, self).__init__()

    def run(self):
        with requests.get(
                url='https://files.minecraftforge.net/net/minecraftforge/forge',
                headers={'User-Agent': user_agent()}
        ) as get:
            html = etree.HTML(get.text)
            version_list = html.xpath('//li[@class="li-version-list"]/ul//li//text()')
            self.result_ready.emit(["forge-"+i.strip() for i in version_list if i.strip() != ''])