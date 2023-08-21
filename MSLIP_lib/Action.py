from abc import ABC, abstractmethod


class Action(ABC):
    """所有方法的基类"""

    @abstractmethod
    def startServer(self) -> None:
        """启动服务器"""

    @abstractmethod
    def DownloadJar(self) -> None:
        """下载.jar文件"""


class BackendMethod(Action):
    def __init__(self, a):
        self.a = a
