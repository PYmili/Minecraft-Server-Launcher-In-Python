from abc import ABC, abstractmethod


class ServerAction(ABC):
    """所有方法的基类"""

    @abstractmethod
    def DownloadJar_official(self) -> None:
        """下载.jar文件"""

    @abstractmethod
    def DownloadJar_spigot(self) -> None:
        """下载.jar文件"""

    @abstractmethod
    def GetJarList(self) -> list:
        """获取当前可用核心列表"""
