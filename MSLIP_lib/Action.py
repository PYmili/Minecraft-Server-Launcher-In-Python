from abc import ABC, abstractmethod


class ServerAction(ABC):
    """所有方法的基类"""

    @abstractmethod
    def Download_official(self) -> None:
        """下载.jar文件"""

    @abstractmethod
    def Download_spigot(self) -> None:
        """下载.jar文件"""

    @abstractmethod
    def Download_forge(self) -> None:
        """下载forge文件"""

    @abstractmethod
    def GetJarList(self) -> list:
        """获取当前可用核心列表"""
