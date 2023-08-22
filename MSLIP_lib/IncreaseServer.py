import subprocess

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox,
    QFileDialog,
    QDesktopWidget,
)

from PyQt5.QtCore import (
    QThread,
    pyqtSignal
)

from BackendMethods import BackendMethod


class AddButtonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SetingSevers")  # 设置窗口标题
        self.setGeometry(0, 0, 480, 270)
        self.setMaximumSize(960, 540)
        self.center_window()

        main_layout = QVBoxLayout()

        # 第一个组
        group1 = QGroupBox()
        layout1 = QVBoxLayout()

        select_file_button = QPushButton("选择java")
        select_file_button.clicked.connect(self.onSelectFileClicked)

        # 查找java的线程
        # AutoSearchJavaThreedResult用于接受返回
        self.AutoSearchJavaThreadResult = ""
        self.AutoSearchJavaThread = JavaLocatorThread()
        self.AutoSearchJavaThread.result_ready.connect(self.AutoSearchJavaThreadEvent)
        AutoSearchJava = QPushButton("自动查找Java")
        AutoSearchJava.clicked.connect(self.AutoSearchJavaThreadEvent)

        self.JavaPathInputBox = QLineEdit()

        layout1.addWidget(select_file_button)
        layout1.addWidget(AutoSearchJava)
        layout1.addWidget(self.JavaPathInputBox)
        group1.setLayout(layout1)

        # 第二个组
        group2 = QGroupBox()
        layout2 = QHBoxLayout()
        self.Xmx = QLineEdit()
        self.Xmx.setText("1024M")
        layout2.addWidget(QLabel("最大内存"))
        layout2.addWidget(self.Xmx)
        layout2.addWidget(QLabel("M/G"))
        group2.setLayout(layout2)

        # 第三个组
        group3 = QGroupBox()
        layout3 = QHBoxLayout()
        self.Xms = QLineEdit()
        self.Xms.setText("1024M")
        layout3.addWidget(QLabel("最小内存"))
        layout3.addWidget(self.Xms)
        layout3.addWidget(QLabel("M/G"))
        group3.setLayout(layout3)

        # 第四个组
        group4 = QGroupBox()
        layout4 = QVBoxLayout()
        self.comboBox = QComboBox()  # 创建下拉菜单
        self.comboBox.addItems(BackendMethod().GetJarList())
        layout4.addWidget(QLabel("选择已下载的框架:"))
        layout4.addWidget(self.comboBox)
        group4.setLayout(layout4)

        main_layout.addWidget(group1)
        main_layout.addWidget(group2)
        main_layout.addWidget(group3)
        main_layout.addWidget(group4)

        self.setLayout(main_layout)

    def onSelectFileClicked(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.input_box.setText(file_path)

    def AutoSearchJavaThreadEvent(self, result: str = False):
        if result:
            self.JavaPathInputBox.setText(result)
        else:
            self.JavaPathInputBox.setText("正在查找...")
            self.AutoSearchJavaThread.start()

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())


class JavaLocatorThread(QThread):
    result_ready = pyqtSignal(str)

    def run(self):
        try:
            # 使用subprocess来运行命令行查找Java路径
            result = subprocess.check_output(['where', 'java']).decode('utf-8')
            self.result_ready.emit(result)
        except subprocess.CalledProcessError:
            self.result_ready.emit("Java路径未找到")