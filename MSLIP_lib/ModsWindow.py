import os
import json

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QDialog,
    QFileDialog,
)

from .TerminalWindow import ServerSelectionWindow
from .BackendMethods import BackendMethod

from loguru import logger


class ModsWindow(QWidget):
    """Mods的管理文件夹"""
    def __init__(self):
        super().__init__()
        self.ServerName = False

        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        button_layout = QVBoxLayout()

        # 创建选择服务器按钮
        select_server_button = QPushButton('选择服务器')
        select_server_button.setStyleSheet('background-color: green')
        select_server_button.clicked.connect(self.select_server)

        add_button = QPushButton('添加Mod')
        add_button.setStyleSheet('background-color: blue')

        delete_button = QPushButton('删除Mod')
        delete_button.setStyleSheet('background-color: red')

        button_layout.addWidget(select_server_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        self.mod_list = QListWidget()

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.mod_list)

        self.setLayout(main_layout)

        # Connect buttons to functions
        add_button.clicked.connect(self.add_mod)
        delete_button.clicked.connect(self.delete_mod)

    def select_server(self) -> None:
        """
        选择要管理的服务器
        :return: None
        """
        self.SeletWindow = ServerSelectionWindow()
        result = self.SeletWindow.exec_()
        if result == QDialog.Accepted:
            with open(r".\Servers\ServerToRun.json", "r", encoding="utf-8") as wfp:
                self.ServerName = json.loads(wfp.read())["ServerName"]

            # 获取服务器的所有mod
            mods = BackendMethod(server_name=self.ServerName).GetServerMods()
            if mods is False:
                return

            # 添加mod的名字至界面列表
            self.mod_list.clear()
            for mod in mods:
                self.add_mod(os.path.split(mod)[-1])

    def add_mod(self, title: str = False) -> None:
        """
        添加一个mod至服务器
        :param title:
        :return: None
        """
        new_mod_item = False

        if title is not False:
            new_mod_item = QListWidgetItem(title)

        # 选择.jar文件添加至服务器mods文件夹
        elif self.ServerName is not False:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "*.jar")
            if os.path.isfile(file_path) is True:
                if BackendMethod(server_name=self.ServerName).AddMod(file_path) is True:
                    logger.info("添加成功！")
                    new_mod_item = QListWidgetItem(f"{os.path.split(file_path)[-1]}")
                else:
                    logger.info("添加失败！")
        else:
            logger.warning("未选择服务器！")
            new_mod_item = QListWidgetItem("未选择服务器！")

        if new_mod_item:
            self.mod_list.addItem(new_mod_item)

    def delete_mod(self) -> None:
        """
        通过列表删除服务器中的mod
        :return: None
        """
        selected_item = self.mod_list.currentItem()
        if selected_item:
            # 删除mod
            if self.ServerName is not False:
                BackendMethod(
                    server_name=self.ServerName
                ).RemoveMod(selected_item.text())

            row = self.mod_list.row(selected_item)
            self.mod_list.takeItem(row)