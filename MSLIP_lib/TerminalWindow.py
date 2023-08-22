import json
import os

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QProcess, QThread, pyqtSignal, QObject


class StartJavaServerProcess(QProcess):
    output_ready = pyqtSignal(str)

    def __init__(self, java_path, server_path, server_args):
        super().__init__()
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self.readOutput)
        self.setProgram(f"cd {os.path.split(server_path)[0]} " + f"\"{java_path}\"" + f" {server_args} -jar {server_path}")
        print(f"cd {os.path.split(server_path)[0]} " + f"\"{java_path}\"" + f" {server_args} -jar {server_path}")
        self.start()

    def readOutput(self):
        output = self.readAllStandardOutput().data().decode("utf-8")
        self.output_ready.emit(output)


class TerminalThread(QThread):
    output_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        with open("./Servers/ServerToRun.json", "r", encoding="utf-8") as rfp:
            data = json.loads(rfp.read())
        self.java_path = data['java']
        self.server_path = data['framework']
        self.server_args = f"-Xmx{data['xmx']} -Xms{data['xms']}"

    def run(self):
        process = StartJavaServerProcess(
            self.java_path,
            self.server_path,
            self.server_args
        )

        while process.waitForReadyRead():
            output = process.readAllStandardOutput().data().decode("utf-8")
            self.output_ready.emit(output)


class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        layout = QVBoxLayout()

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        layout.addWidget(self.terminal_output)

        self.command_input = QLineEdit(self)
        layout.addWidget(self.command_input)

        self.run_command_button = QPushButton("Run Command", self)
        self.run_command_button.clicked.connect(self.runCommand)
        layout.addWidget(self.run_command_button)

        self.start_button = QPushButton("Start Server", self)
        self.start_button.clicked.connect(self.onStartButton)  # 绑定点击事件
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def onStartButton(self):
        self.terminal_thread = TerminalThread()
        self.terminal_thread.output_ready.connect(self.updateTerminalOutput)
        self.terminal_thread.start()

    def updateTerminalOutput(self, output):
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText(output)

    def runCommand(self):
        command = self.command_input.text()
        self.updateTerminalOutput(f"{command}\n")
        self.command_input.clear()