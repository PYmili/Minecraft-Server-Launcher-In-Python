import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QPushButton, QLabel, QDesktopWidget, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt


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


class StartWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.StartButton = QPushButton("启动", self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.StartButton.setFont(QFont("Arial", 14, QFont.Bold))
        self.StartButton.setStyleSheet(
            "QPushButton { background-color: green; color: white; border: none; padding: 10px 20px; }"
            "QPushButton:hover { background-color: darkgreen; }"
            "QPushButton:pressed { background-color: lightgreen; }"
        )
        self.StartButton.setCursor(Qt.PointingHandCursor)

        # 水平布局，将按钮置于右下角
        h_layout = QHBoxLayout()
        h_layout.addStretch()  # 在按钮前面添加一个伸缩项，将按钮推到右侧
        h_layout.addWidget(self.StartButton, alignment=Qt.AlignRight | Qt.AlignBottom)
        layout.addLayout(h_layout)

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

        # 添加左侧菜单按钮
        self.add_menu_item("启动")
        self.add_menu_item("终端")
        self.add_menu_item("下载")
        self.add_menu_item("Mods")

        # 创建右侧子窗口
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(StartWindow())
        self.stacked_widget.addWidget(SubWindow("打开服务器终端"))
        self.stacked_widget.addWidget(SubWindow("下载资源"))
        self.stacked_widget.addWidget(SubWindow("管理Mods"))

        self.current_sub_window_index = 0

        self.menu_list.itemClicked.connect(self.change_sub_window)

        # 布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0，使子窗口完全贴合
        layout.addWidget(self.menu_list, 1)  # 将左侧菜单栏的伸缩因子设置为1
        layout.addWidget(self.stacked_widget, 7)  # 将右侧显示区域的伸缩因子设置为7

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
        selected_index = self.menu_list.row(item)
        if selected_index != self.current_sub_window_index:
            self.stacked_widget.setCurrentIndex(selected_index)
            self.current_sub_window_index = selected_index

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
