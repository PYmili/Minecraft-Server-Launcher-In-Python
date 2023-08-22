import json
import os
import shutil
import subprocess
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox,
    QFileDialog,
    QDesktopWidget,
    QMessageBox,
)

from PyQt5.QtCore import (
    QThread,
    pyqtSignal
)

from .BackendMethods import BackendMethod


class AddButtonWindow(QWidget):
    """添加服务器配置界面"""
    def __init__(self, UpdateCardFun: object):
        """
        :param UpdateCardFun: 用于添加成功后更新CreateWindow中的卡片
        """
        super().__init__()
        self.UpdataCardFun = UpdateCardFun

        self.setWindowTitle("SetingSevers")  # 设置窗口标题
        self.setGeometry(0, 0, 480, 270)
        # self.setMaximumSize(960, 540)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

        # 设置样式表
        self.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QGroupBox {
            border: 1px solid gray;
            border-radius: 4px;
            margin-top: 8px;
            padding: 8px;
        }
        """)

        main_layout = QVBoxLayout()

        # 第一个组
        group1 = QGroupBox()
        layout1 = QVBoxLayout()

        select_file_button = QPushButton("选择java")
        select_file_button.clicked.connect(self.onSelectFileClicked)

        # 查找java的线程
        # AutoSearchJavaThreedResult用于接受返回
        self.AutoSearchJavaThreadResult = ""
        self.AutoSearchJavaThread = JavaLocatorThread()
        self.AutoSearchJavaThread.result_ready.connect(self.AutoSearchJavaThreadEvent)
        AutoSearchJava = QPushButton("自动查找Java")
        AutoSearchJava.clicked.connect(self.AutoSearchJavaThreadEvent)
        self.JavaPathInputBox = QLineEdit()
        layout1.addWidget(select_file_button)
        layout1.addWidget(AutoSearchJava)
        layout1.addWidget(self.JavaPathInputBox)
        group1.setLayout(layout1)

        # 第二个组
        group2 = QGroupBox()
        layout2 = QHBoxLayout()
        self.Xmx = QLineEdit()
        self.Xmx.setText("1024M")
        layout2.addWidget(QLabel("最大内存"))
        layout2.addWidget(self.Xmx)
        layout2.addWidget(QLabel("M/G"))
        group2.setLayout(layout2)

        # 第三个组
        group3 = QGroupBox()
        layout3 = QHBoxLayout()
        self.Xms = QLineEdit()
        self.Xms.setText("1024M")
        layout3.addWidget(QLabel("最小内存"))
        layout3.addWidget(self.Xms)
        layout3.addWidget(QLabel("M/G"))
        group3.setLayout(layout3)

        # 第四个组
        group4 = QGroupBox()
        layout4 = QVBoxLayout()
        self.comboBox = QComboBox()  # 创建下拉菜单
        self.comboBox.addItems(BackendMethod().GetJarList())
        layout4.addWidget(QLabel("选择已下载的框架:"))
        layout4.addWidget(self.comboBox)
        group4.setLayout(layout4)

        # 第五个
        group5 = QGroupBox()
        layout5 = QHBoxLayout()
        self.setServerName = QLineEdit()
        layout5.addWidget(QLabel("服务器名字："))
        layout5.addWidget(self.setServerName)
        group5.setLayout(layout5)

        # 第六个组
        group6 = QGroupBox()
        layout6 = QHBoxLayout()
        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.onConfirmClicked)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.close)
        layout6.addWidget(confirm_button)
        layout6.addWidget(cancel_button)
        group6.setLayout(layout6)

        main_layout.addWidget(group1)
        main_layout.addWidget(group2)
        main_layout.addWidget(group3)
        main_layout.addWidget(group4)
        main_layout.addWidget(group5)
        main_layout.addWidget(group6)

        self.setLayout(main_layout)

        self.NewServer = None

    # 选择java的事件
    def onSelectFileClicked(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.JavaPathInputBox.setText(file_path)

    # 自动选择java
    def AutoSearchJavaThreadEvent(self, result: str = False):
        if result:
            self.JavaPathInputBox.setText(result)
        else:
            self.JavaPathInputBox.setText("正在查找...")
            self.AutoSearchJavaThread.start()

    # 点击确认，创建服务器事件
    def onConfirmClicked(self):
        # 用于存放新服务器的参数
        new_server_data = {
            "ServerName": str(self.setServerName.text()),
            "java": str(self.JavaPathInputBox.text().strip('\r\n')),
            "framework": str(self.comboBox.currentText()),
            "xmx": str(self.Xmx.text()),
            "xms": str(self.Xms.text())
        }
        errorMsg = ""
        if len(new_server_data['java']) == 0:
            errorMsg = "未选择Java"
        elif len(new_server_data['xmx']) == 0 or len(new_server_data['xms']) == 0:
            errorMsg = "请设置内存"
        elif len(new_server_data['ServerName']) == 0:
            errorMsg = "未设置名字！"

        if errorMsg:
            QMessageBox.warning(
                self, "错误", errorMsg,
                QMessageBox.Yes
            )
            return
        # 创建新服务器线程，并且附带返回值
        self.NewServer = NewServerThread(new_server_data)
        self.NewServer.result_ready.connect(self.NewServerThreadEvent)
        self.NewServer.start()

    # 判断服务器是否创建成功，并且返回结果。
    def NewServerThreadEvent(self, result: str):
        QMessageBox.information(
            self, "结果", result,
            QMessageBox.Yes
        )
        if result == "创建成功！":
            # 更新卡片，关闭窗口
            self.UpdataCardFun()
            self.close()


class JavaLocatorThread(QThread):
    """查找java路径线程"""
    result_ready = pyqtSignal(str)

    def run(self):
        try:
            # 使用subprocess来运行命令行查找Java路径
            result = subprocess.check_output(['where', 'java']).decode('utf-8')
            self.result_ready.emit(result)
        except subprocess.CalledProcessError:
            self.result_ready.emit("Java路径未找到")


class NewServerThread(QThread):
    """创建新服务器线程"""
    result_ready = pyqtSignal(str)

    def __init__(self, NewServerData: dict):
        """
        :param NewServerData: dict数据，存放新服务器的参数
        """
        super(NewServerThread, self).__init__(parent=None)
        self.NewServerData = NewServerData

    def run(self):
        # 当前时间，用于显示服务器创建时间。
        present_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        rfp = open("./Servers/Servers.json", "r", encoding="utf-8")
        ServersRead = json.loads(rfp.read())
        rfp.close()

        try:
            if os.path.isdir(f"./Servers/{self.NewServerData['ServerName']}") is True:
                self.result_ready.emit("服务器文件夹已存在！")
                return
            # 在Servers文件夹中创建服务器名字的文件夹
            os.mkdir(f"./Servers/{self.NewServerData['ServerName']}")
            if os.path.isfile(self.NewServerData['framework']) is False:
                self.result_ready.emit(f"“{self.NewServerData['framework']}”文件不存在！")

            # 复制用户指定的服务器内核至服务器名字的文件夹
            shutil.copy(
                self.NewServerData['framework'],
                f"./Servers/{self.NewServerData['ServerName']}"
            )

            # 更新服务器内核的位置
            self.NewServerData[
                'framework'
            ] = os.path.join(
                f".\\Servers\\{self.NewServerData['ServerName']}",
                os.path.split(self.NewServerData['framework'])[-1]
            )

            self.NewServerData["CreationTime"] = present_time
            ServersRead[self.NewServerData['ServerName']] = self.NewServerData
            with open("./Servers/Servers.json", "w+", encoding="utf-8") as wfp:
                wfp.write(json.dumps(ServersRead, indent=4))

            self.result_ready.emit("创建成功！")
        except Exception as e:
            self.result_ready.emit(f"创建失败！", e)
