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

    @abstractmethod
    def GetJarList(self) -> list:
        "获取当前可用核心列表"


class BackendMethod(Action):
    def __init__(self, spigot_v: str, xmx: str, xms: str):
        """
        spigot_v:服务器名称+spigot版本,由gui传入,格式:name_version
        xmx:最大内存
        xms:最小内存
        """
        self.spigot_v = spigot_v
        self.xmx = xmx
        self.xms = xms

    def startServer(self) -> None:
        """此函数由启动服务器事件调用"""
        with open(r'../Servers/Test_1.18/test.txt', 'r', encoding='utf-8') as fr:
            f = fr.read()
            print(f)
        subprocess.Popen(f'java -{self.xmx} -{self.xms} -jar ../Servers/{self.spigot_v}/spigot', shell=True)

    def DownloadJar(self) -> None:
        """此方法由下载事件调用"""
        pass


b = BackendMethod(spigot_v='a', xms='a', xmx='s')
b.startServer()
