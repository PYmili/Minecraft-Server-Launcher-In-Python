import sys
import json
import os

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QLabel,
    QDesktopWidget,
    QStackedWidget,
    QGroupBox,
    QGridLayout
)
from PyQt5.QtGui import (
    QFont,
    QPalette,
    QBrush,
    QPixmap
)
from PyQt5.QtCore import (
    QSize,
    Qt
)

# 添加服务器界面
from IncreaseServer import AddButtonWindow


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
        self.add_button_window = None
        self.StartButton = QPushButton("启动", self)
        self.AddButton = QPushButton("添加", self)
        self.gridLayout = QGridLayout()  # 使用 QGridLayout 作为网格布局
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # 设置启动按钮样式
        self.StartButton.setFont(QFont("Arial", 14, QFont.Bold))
        self.StartButton.setStyleSheet(
            "QPushButton { background-color: green; color: white; border: none; padding: 10px 20px; }"
            "QPushButton:hover { background-color: darkgreen; }"
            "QPushButton:pressed { background-color: lightgreen; }"
        )
        self.StartButton.setCursor(Qt.PointingHandCursor)

        # 设置添加按钮样式
        self.AddButton.setFont(QFont("Arial", 14, QFont.Bold))
        self.AddButton.setStyleSheet(
            "QPushButton { background-color: blue; color: white; border: none; padding: 10px 20px; }"
            "QPushButton:hover { background-color: darkblue; }"
            "QPushButton:pressed { background-color: lightcoral; }"
        )
        self.AddButton.setCursor(Qt.PointingHandCursor)
        self.AddButton.clicked.connect(self.addButtonShow)  # 连接添加按钮的点击事件

        # 创建一个 QGroupBox 来包含按钮布局
        button_group = QGroupBox()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.AddButton, alignment=Qt.AlignRight | Qt.AlignBottom)
        button_layout.addWidget(self.StartButton, alignment=Qt.AlignRight | Qt.AlignBottom)
        button_group.setLayout(button_layout)
        button_group.setStyleSheet("QGroupBox { border: none; }")

        # 添加网格布局到主垂直布局
        main_layout.addLayout(self.gridLayout)

        # 添加按钮组到主垂直布局
        main_layout.addWidget(button_group)

        self.setLayout(main_layout)

        self.UpdateCard()

    def addButtonShow(self) -> None:
        self.add_button_window = AddButtonWindow(self.UpdateCard)
        self.add_button_window.show()
        
    def UpdateCard(self) -> None:
        with open("Servers.json", "r", encoding="utf-8") as rfp:
            ServerData = json.loads(rfp.read())
            
        for i in ServerData.keys():
            self.addCard(
                ServerData[i]['ServerName'] +
                "\n使用框架：" +
                os.path.split(ServerData[i]['framework'])[-1] +
                "\n创建时间：" +
                ServerData[i]['CreationTime']
            )

    def addCard(self, text: str):
        card_button = QPushButton(text, self)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        card_button.setFont(font)
        card_button.setStyleSheet(
            "QPushButton { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #3399FF, stop: 1 #0066CC);"
            "border-radius: 5px; padding: 10px; color: white; }"
            "QPushButton:hover { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #55aaff, stop: 1 #3399FF); }"
            "QPushButton:pressed { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #0066CC, stop: 1 #004499); }"
        )

        self.gridLayout.addWidget(card_button)  # 在网格中添加卡片按钮


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minecraft 服务器启动器")
        self.setGeometry(100, 100, 960, 540)

        # 居中窗口
        self.center_window()

        # 设置整个窗口的样式表
        # self.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")

        # 创建左侧菜单
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("border: none; background-color: rgb(50, 50, 50); color: white;")

        # 添加左侧菜单按钮
        self.add_menu_item("启动", 0)
        self.add_menu_item("终端", 1)
        self.add_menu_item("下载", 2)
        self.add_menu_item("Mods", 3)

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
        layout.addWidget(self.stacked_widget, 10)  # 将右侧显示区域的伸缩因子设置为

        self.menu_list.setStyleSheet(
            "QListWidget { border: none; background-color: rgb(50, 50, 50); color: white; }"
            "QListWidget::item { padding: 15px; }"
            "QListWidget::item:selected { background-color: rgb(80, 80, 80); color: white; }"  # 选中效果
        )

    def add_menu_item(self, text, index):
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

        # 使用临时变量来传递 sub_windows
        button.clicked.connect(lambda :self.Button_sub_window(index))

    def Button_sub_window(self, index):
        if index != self.current_sub_window_index:
            self.stacked_widget.setCurrentIndex(index)
            self.current_sub_window_index = index

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

    def updateBackgroundImage(self, img_path):
        palette = QPalette()
        pix = QPixmap(img_path)

        pix = pix.scaled(self.width(), self.height())

        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    # 重写窗口的 resizeEvent 方法
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 在窗口大小变化时更新背景图片
        self.updateBackgroundImage("../resources/images/bg_0.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())