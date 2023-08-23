from PyQt5.QtCore import QSize
from PyQt5.QtGui import (
    QFont,
    QPalette,
    QBrush,
    QPixmap
)
from PyQt5.QtWidgets import (
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
)
from loguru import logger

from .CreateWindow import CreateWindow
from .Jar_DownLoad import JarDownLoad
from .TerminalWindow import TerminalWindow


class SubWindow(QWidget):
    """切换界面测试"""
    def __init__(self, content):
        super().__init__()
        self.content = content
        self.initUI()
        logger.info("切换界面测试")

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel(self.content)
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主界面"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minecraft 服务器启动器")
        self.setGeometry(100, 100, 960, 540)

        # 居中窗口
        self.center_window()

        # 创建左侧菜单
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("border: none; background-color: rgb(50, 50, 50); color: white;")

        # 添加左侧菜单按钮
        self.add_menu_item("创建", 0)
        self.add_menu_item("启动", 1)
        self.add_menu_item("下载", 2)
        self.add_menu_item("Mods", 3)

        # 创建右侧子窗口
        self.stacked_widget = QStackedWidget()
        self.Create = CreateWindow()
        self.Terminal = TerminalWindow()
        self.Jar_ = JarDownLoad()

        self.stacked_widget.addWidget(self.Jar_)
        self.stacked_widget.addWidget(self.Create)
        self.stacked_widget.addWidget(self.Terminal)
        self.stacked_widget.addWidget(SubWindow("下载资源"))
        self.stacked_widget.addWidget(SubWindow("管理Mods"))

        self.current_sub_window_index = 0   # 记录当前界面是哪一个
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
        logger.info("启动程序主界面")

    def add_menu_item(self, text, index):
        logger.info("添加左侧菜单按钮")
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

    # 点击QListWidget中的按钮，切换QStackedWidget窗口
    def Button_sub_window(self, index):
        logger.info(f"QStackedWidget窗口为：{index}")
        if index != self.current_sub_window_index:
            self.stacked_widget.setCurrentIndex(index)
            self.current_sub_window_index = index

    # 点击QListWidget，切换QStackedWidget中的窗口
    def change_sub_window(self, item):
        selected_index = self.menu_list.row(item)
        logger.info(f"QStackedWidget中的窗口为：{selected_index}")
        if selected_index != self.current_sub_window_index:
            self.stacked_widget.setCurrentIndex(selected_index)
            self.current_sub_window_index = selected_index

    # 居中窗口方法
    def center_window(self):
        logger.info("居中窗口")
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    # 更新 背景图片 的方法
    def updateBackgroundImage(self, img_path):
        logger.info("更新背景图片")
        palette = QPalette()
        pix = QPixmap(img_path)
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    # 重写窗口的 resizeEvent 方法
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 在窗口大小变化时更新背景图片
        self.updateBackgroundImage("./resources/images/bg_0.png")

    def closeEvent(self, event):
        logger.info("程序结束")
        event.accept()