from abc import ABC, abstractmethod


class ServerAction(ABC):
    """所有方法的基类"""

    @abstractmethod
    def Download_official(self) -> bool:
        """下载.jar文件"""

    @abstractmethod
    def Download_spigot(self) -> bool:
        """下载.jar文件"""

    @abstractmethod
    def Download_forge(self) -> bool:
        """下载forge文件"""

    @abstractmethod
    def GetJarList(self) -> list:
        """获取当前可用核心列表"""

    @abstractmethod
    def GetOfficialGameServerList(self) -> list:
        """获取官方游戏内核可下载版本"""

    @abstractmethod
    def GetServerMods(self) -> list:
        """获取服务器中所有mod"""

    @abstractmethod
    def AddMod(self, ModPath: str) -> bool:
        """给服务器添加mod"""

    @abstractmethod
    def RemoveMod(self, ModName: str) -> bool:
        """删除服务器mod"""
