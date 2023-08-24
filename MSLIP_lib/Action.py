from abc import ABC, abstractmethod


class ServerAction(ABC):
    """所有方法的基类"""

    @abstractmethod
    def Download_official(self):
        """下载.jar文件"""

    @abstractmethod
    def Download_spigot(self):
        """下载.jar文件"""

    @abstractmethod
    def Download_forge(self):
        """下载forge文件"""

    @abstractmethod
    def GetJarList(self) -> list:
        """获取当前可用核心列表"""

    @abstractmethod
    def GetOfficialGameServerList(self) -> list:
        """获取官方游戏内核可下载版本"""
