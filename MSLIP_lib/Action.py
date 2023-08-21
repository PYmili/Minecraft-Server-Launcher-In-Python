import subprocess
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
    def __init__(self, ser_name: str = 'Test_1.18',
                 server_v: str = '1.18',
                 xmx: str = '4096',
                 xms: str = '2048',
                 select_v: str = '1.18',
                 ):
        """
        ser_name:服务器名称
        server_v:服务器框架版本
        xmx:最大内存
        xms:最小内存
        """
        self.ser_name = ser_name
        self.server_v = server_v
        self.select_v = select_v
        self.spigot_url = f'https://mcversions.net/download/{self.select_v}'
        self.xmx = xmx
        self.xms = xms

    def startServer(self) -> None:
        """此函数由启动服务器事件调用"""
        subprocess.Popen(f'java -{self.xmx} -{self.xms} -jar ../Servers/{self.ser_name}/server.jar',
                         shell=True)

    def DownloadJar(self) -> None:
        """此方法由下载事件调用"""

        pass


b = BackendMethod()
b.DownloadJar()
