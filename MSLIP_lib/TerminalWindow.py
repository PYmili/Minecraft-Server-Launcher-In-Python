import json
import os

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QComboBox,
    QDesktopWidget,
    QDialog,
)
from PyQt5.QtCore import (
    QProcess,
    QThread,
    pyqtSignal
)

from .BackendMethods import BackendMethod
from loguru import logger


class StartJavaServerProcess(QProcess):
    """使用QProcess启动Java版服务器，有输入命令，输出游戏log功能"""
    output_ready = pyqtSignal(str)

    def __init__(self, java_path, server_path, server_args):
        """
        :param java_path: java路径
        :param server_path: 服务器内核路径
        :param server_args: 启动参数
        """
        super().__init__()
        logger.info("启动StartJavaServerProcess")
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self.readOutput)

        # 提前加载eula协议
        self.eulaTxt = os.path.join(os.path.split(server_path)[0], "eula.txt")
        with open(self.eulaTxt, "w+", encoding="utf-8") as wfp:
            wfp.write("eula=true\n")

        logger.info(f"cd {os.path.dirname(server_path)}")
        self.setWorkingDirectory(os.path.dirname(server_path))  # 设置工作目录为服务器文件所在目录

        self.start(java_path, server_args + ["-jar", os.path.basename(server_path), "nogui"])
        logger.info(f"{java_path} {' '.join(server_args)} -jar {os.path.basename(server_path)} nogui")

    # 读取游戏log输出
    def readOutput(self):
        output = self.readAllStandardOutput().data().decode("utf-8")
        logger.info(output)
        self.output_ready.emit(output)

    # 发送命令
    def writeCommand(self, command):
        logger.info(f"发送命令:{command}".encode("utf-8"))
        self.write(f"{command}\n".encode("utf-8"))


class TerminalThread(QThread):
    """终端显示程序，调用StartJavaServerProcess"""
    output_ready = pyqtSignal(str)
    send_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        with open("./Servers/ServerToRun.json", "r", encoding="utf-8") as rfp:
            data = json.loads(rfp.read())
        self.java_path = data['java']
        self.server_path = data['framework']
        self.server_args = [
            f"-Xmx{data['xmx']}",
            f"-Xms{data['xms']}"
        ]

    def run(self):
        logger.info("启动TerminalThread")
        self.process = StartJavaServerProcess(
            self.java_path,
            self.server_path,
            self.server_args
        )

        self.process.output_ready.connect(self.getOutput)

        while self.process.waitForReadyRead():
            pass

    # 发送log信息
    def getOutput(self, result):
        self.output_ready.emit(result)

    # 发送命令
    def sendCommand(self, command):
        if self.process:
            self.process.writeCommand(command)


class TerminalWindow(QWidget):
    """启动和终端界面"""
    def __init__(self):
        super().__init__(parent=None)
        logger.info("启动和终端界面")
        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        # 显示游戏内核的log输出
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        left_layout.addWidget(self.terminal_output)

        input_layout = QHBoxLayout()
        # 命令输入
        self.command_input = QLineEdit(self)
        input_layout.addWidget(self.command_input)

        # 运行命令的按钮
        self.run_command_button = QPushButton("输入", self)
        self.run_command_button.clicked.connect(self.runCommand)
        input_layout.addWidget(self.run_command_button)

        left_layout.addLayout(input_layout)
        main_layout.addLayout(left_layout)

        # 右侧组布局，有显示所有可用命令和启动服务器按钮
        offside_layout = QVBoxLayout()
        group_box = QGroupBox("命令列表")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        self.start_button = QPushButton("启动服务器", self)
        self.start_button.clicked.connect(self.onStartButton)
        offside_layout.addWidget(group_box)
        offside_layout.addWidget(self.start_button)
        main_layout.addLayout(offside_layout)

        self.setLayout(main_layout)

        # 设置样式表
        self.setStyleSheet("""
        QWidget {
            background-color: #34495e;
            color: white;
        }
        QTextEdit {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #2980b9;
            padding: 5px;
        }

        QLineEdit {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #2980b9;
            padding: 5px;
        }

        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }

        QPushButton:hover {
            background-color: #2980b9;
        }

        QGroupBox {
            border: 1px solid #2980b9;
            border-radius: 5px;
            margin-top: 20px;
        }
        """)

    # 打开服务器选择的界面
    def onStartButton(self):
        logger.info("打开服务器选择界面")
        self.serverSelection = ServerSelectionWindow()
        result = self.serverSelection.exec_()  # 显示模态对话框，阻塞主界面
        if result == QDialog.Accepted:
            self.terminal_thread = TerminalThread()
            self.terminal_thread.output_ready.connect(self.updateTerminalOutput)
            self.terminal_thread.start()
            self.terminal_output.clear()

    # 更新QlineEdit中的log输出
    def updateTerminalOutput(self, output):
        logger.info("更新QlineEdit中的log输出")
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText(output)

    # 运行命令事件
    def runCommand(self):
        command = self.command_input.text()
        self.command_input.clear()

        if hasattr(self, 'terminal_thread'):
            self.terminal_thread.sendCommand(command)


class ServerSelectionWindow(QDialog):
    """服务器选择界面"""
    def __init__(self):
        super().__init__()

        logger.info("已打开服务器选择界面")

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
        confirm_button.clicked.connect(self.confirmSelection)
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

    def confirmSelection(self):
        logger.info("确认要启动服务器")
        selected_server = self.server_combo_box.currentText()
        writeData = self.getServerList()[selected_server]
        writeData['framework'] = os.path.join(
            os.getcwd(),
            writeData['framework'].strip(".\\")
        )
        with open("./Servers/ServerToRun.json", "w+", encoding="utf-8") as wfp:
            wfp.write(json.dumps(writeData, indent=4))

        self.accept()
        self.close()

