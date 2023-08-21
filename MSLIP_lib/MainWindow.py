import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QPushButton, QLabel, QDesktopWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize


class SubWindow(QWidget):
    def __init__(self, content):
        super().__init__()
        self.content = content
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel(self.content)
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minecraft 服务器启动器")
        self.setGeometry(100, 100, 800, 600)

        # 居中窗口
        self.center_window()

        # 设置整个窗口的样式表
        self.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")

        # 创建左侧菜单
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("border: none; background-color: rgb(50, 50, 50); color: white;")

        # 创建右侧子窗口
        self.sub_windows = {
            "启动": SubWindow("启动服务器"),
            "终端": SubWindow("打开服务器终端"),
            "下载": SubWindow("下载资源"),
            "Mods": SubWindow("管理Mods"),
        }

        self.current_sub_window = None

        self.menu_list.itemClicked.connect(self.change_sub_window)

        # 布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0，使子窗口完全贴合
        layout.addWidget(self.menu_list, 1)  # 将左侧菜单栏的伸缩因子设置为1
        self.display_widget = QWidget()
        layout.addWidget(self.display_widget, 7)  # 将右侧显示区域的伸缩因子设置为7

        self.display_layout = QVBoxLayout(self.display_widget)
        self.display_layout.addWidget(self.sub_windows["启动"])
        self.current_sub_window = self.sub_windows["启动"]

        # 添加左侧菜单按钮
        self.add_menu_item("启动")
        self.add_menu_item("终端")
        self.add_menu_item("下载")
        self.add_menu_item("Mods")

        self.menu_list.setStyleSheet(
            "QListWidget { border: none; background-color: rgb(50, 50, 50); color: white; }"
            "QListWidget::item { padding: 15px; }"
            "QListWidget::item:selected { background-color: rgb(80, 80, 80); color: white; }"  # 选中效果
        )

    def add_menu_item(self, text):
            button = QPushButton(text)
            button.setFont(QFont("Arial", 12, QFont.Bold))  # 设置按钮字体样式
            button.setStyleSheet(
                "QPushButton { background-color: transparent; border: none; color: white; }"
                "QPushButton:pressed { background-color: rgb(80, 80, 80); }"  # 按下效果
            )
            item = QListWidgetItem()
            self.menu_list.addItem(item)
            self.menu_list.setItemWidget(item, button)
            item.setSizeHint(QSize(item.sizeHint().width(), 50))  # 调整按钮高度

    def change_sub_window(self, item):
        selected_text = self.menu_list.itemWidget(item).text()
        if selected_text in self.sub_windows:
            new_sub_window = self.sub_windows[selected_text]
            if new_sub_window != self.current_sub_window:
                self.display_layout.removeWidget(self.current_sub_window)
                self.current_sub_window.hide()
                self.display_layout.addWidget(new_sub_window)
                new_sub_window.show()
                self.current_sub_window = new_sub_window

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
