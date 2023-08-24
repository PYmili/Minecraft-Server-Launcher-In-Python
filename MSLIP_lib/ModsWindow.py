from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor


class ModsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('My World Mods Management')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        add_button = QPushButton('Add Mod')
        add_button.setStyleSheet('background-color: blue')
        delete_button = QPushButton('Delete Mod')
        delete_button.setStyleSheet('background-color: red')
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        self.mod_list = QListWidget()

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.mod_list)

        self.setLayout(main_layout)

        # Connect buttons to functions
        add_button.clicked.connect(self.add_mod)
        delete_button.clicked.connect(self.delete_mod)

    def add_mod(self):
        new_mod_item = QListWidgetItem('New Mod')
        self.mod_list.addItem(new_mod_item)

    def delete_mod(self):
        selected_item = self.mod_list.currentItem()
        if selected_item:
            row = self.mod_list.row(selected_item)
            self.mod_list.takeItem(row)
