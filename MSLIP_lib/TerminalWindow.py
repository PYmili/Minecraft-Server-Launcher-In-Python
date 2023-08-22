from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time


class TerminalThread(QThread):
    output_ready = pyqtSignal(str)

    def run(self):
        pass


class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        layout.addWidget(self.terminal_output)

        self.command_input = QLineEdit(self)
        layout.addWidget(self.command_input)

        self.run_command_button = QPushButton("Run Command", self)
        self.run_command_button.clicked.connect(self.runCommand)
        layout.addWidget(self.run_command_button)

        self.setLayout(layout)

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