import json
import os

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QGroupBox
from PyQt5.QtCore import QProcess, QThread, pyqtSignal


class StartJavaServerProcess(QProcess):
    output_ready = pyqtSignal(str)

    def __init__(self, java_path, server_path, server_args):
        super().__init__()
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self.readOutput)
        self.setWorkingDirectory(os.path.dirname(server_path))  # 设置工作目录为服务器文件所在目录
        self.start(java_path, server_args + ["-jar", os.path.basename(server_path), "nogui"])

    def readOutput(self):
        output = self.readAllStandardOutput().data().decode("utf-8")
        self.output_ready.emit(output)

    def writeCommand(self, command):
        self.write(f"{command}\n".encode("utf-8"))


class TerminalThread(QThread):
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
        self.process = StartJavaServerProcess(
            self.java_path,
            self.server_path,
            self.server_args
        )

        self.process.output_ready.connect(self.getOutput)

        while self.process.waitForReadyRead():
            pass

    def getOutput(self, result):
        self.output_ready.emit(result)

    def sendCommand(self, command):
        if self.process:
            self.process.writeCommand(command)


class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        left_layout.addWidget(self.terminal_output)

        input_layout = QHBoxLayout()

        self.command_input = QLineEdit(self)
        input_layout.addWidget(self.command_input)

        self.run_command_button = QPushButton("输入", self)
        self.run_command_button.clicked.connect(self.runCommand)
        input_layout.addWidget(self.run_command_button)

        left_layout.addLayout(input_layout)
        main_layout.addLayout(left_layout)

        # 右侧组布局
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

    def onStartButton(self):
        self.terminal_thread = TerminalThread()
        self.terminal_thread.output_ready.connect(self.updateTerminalOutput)
        self.terminal_thread.start()

    def updateTerminalOutput(self, output):
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText(output)

    def runCommand(self):
        command = self.command_input.text()
        self.command_input.clear()

        if hasattr(self, 'terminal_thread'):
            self.terminal_thread.sendCommand(command)
