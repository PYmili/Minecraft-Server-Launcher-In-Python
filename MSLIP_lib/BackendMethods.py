import os
import shutil

import requests
from fake_user_agent import user_agent
from lxml import etree
from loguru import logger

from .Action import ServerAction


class BackendMethod(ServerAction):
    def __init__(self, server_name: str = False,
                 server_version: str = False,
                 ):
        """
        :param server_name: 选择启动的服务器名称
        :param server_version: 选择下载的服务器版本
        """
        self.ServerName = server_name
        self.ServerVersion = server_version
        self.currentFolder = os.path.join(
            os.path.split(os.path.split(__file__)[0])[0],
            r"Servers\DownLoads\jar"
        )

        self.official_url = 'https://launcher.mojang.com/v1/objects/'
        self.manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        self.spigot_url = f'https://download.getbukkit.org/spigot/spigot-{self.ServerVersion}.jar'
        self.forge_url = f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{self.ServerVersion}.html'
        self.requests_head = {'User-Agent': user_agent()}

    def Download_official(self) -> bool:
        """
        此方法由下载事件调用：下载官方server
        :return: str
        """
        logger.info(f'Download_official: {self.ServerVersion}')
        with requests.get(self.manifest_url) as manifest_get:
            if manifest_get.status_code != 200:
                logger.error("无法获取版本清单。")
                manifest_get.close()
                return False
            else:
                manifestJson = manifest_get.json()

        selected_version = None
        for entry in manifestJson["versions"]:
            if entry["id"] == self.ServerVersion:
                selected_version = entry
                break

        if selected_version is None:
            logger.error("版本无效")
            return False

        # 获取下载链接
        with requests.get(selected_version["url"]) as DownloadResponse:
            if DownloadResponse.status_code != 200:
                logger.error("获取下载链接错误！")
                return False

            DownloadUrl = DownloadResponse.json()["downloads"]["server"]["url"]

        # 下载
        with requests.get(DownloadUrl, stream=True) as jar_response:
            if jar_response.status_code != 200:
                logger.error("无法获取JAR文件。")
                jar_response.close()
                return False

            # 检查和创建文件夹
            __path = os.path.join(self.currentFolder, 'official_hub')
            if os.path.isdir(__path) is False:
                try:
                    os.mkdir(__path)
                except Exception as e:
                    logger.error(f"下载官方框架时检查和创建文件夹出错：{e}")
                    jar_response.close()
                    return False

            # 保存.jar文件
            jar_filename = os.path.join(
                r"Servers\DownLoads\jar\official_hub",
                selected_version["id"] + ".jar"
            )
            with open(jar_filename, "wb") as f:
                for chunk in jar_response.iter_content(8192):
                    f.write(chunk)

        return True

    def Download_spigot(self) -> bool:
        """
        此方法由下载事件调用：下载spigot
        :return: bool
        """
        logger.info(f'Download_forge: {self.ServerVersion}')

        with requests.get(
                url=self.spigot_url,
                headers=self.requests_head,
                stream=True
        ) as spigotRequests:
            if spigotRequests.status_code != 200:
                logger.error("发送请求失败！")
                spigotRequests.close()
                return False

            # 检查和创建文件夹
            __path = os.path.join(self.currentFolder, 'spigot_hub')
            if os.path.isdir(__path) is False:
                try:
                    os.mkdir(__path)
                except Exception as e:
                    logger.error(f"下载Spigot时检查和创建文件夹出错：{e}")
                    spigotRequests.close()
                    return False

            # 保存.jar文件
            filePath = os.path.join(__path, f"{self.ServerVersion}.jar")
            if os.path.isfile(filePath) is False:
                with open(filePath, 'wb') as wfp:
                    for chunk in spigotRequests.iter_content(8192):
                        wfp.write(chunk)
            else:
                logger.info("此版本已存在，不再进行下载。")

        return True

    def Download_forge(self) -> bool:
        """此方法由下载事件调用：下载forge"""
        logger.info(f'Download_forge: {self.ServerVersion}')

        with requests.get(
                url=self.forge_url,
                headers=self.requests_head
        ) as forgeRequests:
            if forgeRequests.status_code != 200:
                logger.error("发送请求失败！")
                forgeRequests.close()
                return False

            # 检查和创建文件夹
            __path = os.path.join(self.currentFolder, 'Forge')
            if os.path.isdir(__path) is False:
                try:
                    os.mkdir(__path)
                except Exception as e:
                    logger.error(f"下载Spigot时检查和创建文件夹出错：{e}")
                    forgeRequests.close()
                    return False

            # 抓取最新版本
            html = etree.HTML(forgeRequests.text)
            version = html.xpath('//div[@class="title"]/small/text()')[0].replace(" ", "")
            forge_url = f'https://maven.minecraftforge.net/net/minecraftforge/forge/' \
                        f'{version}/forge-{version}-installer.jar'
            logger.info(forge_url)

            # 下载.jar文件
            filePath = os.path.join(__path, os.path.split(forge_url)[-1])
            if os.path.isfile(filePath) is False:
                with requests.get(
                        url=forge_url,
                        headers=self.requests_head,
                        stream=True
                ) as jar_req:
                    if jar_req.status_code != 200:
                        logger.error("发送下载.jar请求失败！")
                        return False
                    with open(filePath, 'wb') as wfp:
                        for chunk in jar_req.iter_content(8192):
                            wfp.write(chunk)
            else:
                logger.info("此版本已存在，不再进行下载。")

        return True

    def GetJarList(self) -> list:
        """返回可用版本列表"""
        result = []
        for paths, dirs, files in os.walk(r'.\Servers\DownLoads\Jar'):
            for file in files:
                if os.path.splitext(file)[-1] == ".jar":
                    result.append(os.path.join(paths, file))

        return result

    def GetOfficialGameServerList(self) -> list:
        """
        获取官方服务器所有版本列表
        :return: list
        """
        result = []
        with requests.get(self.manifest_url) as response:
            if response.status_code != 200:
                logger.error("无法获取JAR文件。")
                return []
            responseJson = response.json()
            for entry in responseJson["versions"]:
                if entry['type'] == 'release':
                    result.append(entry['id'])

        return result

    def GetServerMods(self) -> list:
        """
        获取服务器中的所有mod
        :return: list
        """
        logger.info(f"获取{self.ServerName}中的mod")
        result = []
        __path = GetServerPath(self.ServerName)
        if __path is False:
            return False

        __path = ModsDirEvent(__path)
        if __path is False:
            return False

        for paths, dirs, files in os.walk(__path):
            for file in files:
                result.append(os.path.join(paths, file))

        logger.info("获取成功！")
        return result

    def AddMod(self, ModPath: str) -> bool:
        """
        添加mod
        :param ModPath: str
        :return: bool
        """
        logger.info(f"添加{ModPath}至{self.ServerName}")
        __path = GetServerPath(self.ServerName)
        if __path is False:
            return False

        if os.path.isfile(ModPath) is False:
            logger.error(f"{ModPath}不存在！")
            return False

        __path = ModsDirEvent(__path)
        if __path is False:
            return False

        # 复制mod至服务器的mods文件夹
        try:
            shutil.copy(ModPath, __path)
        except Exception as e:
            logger.error(f"复制{ModPath}至{__path}程序错误：{e}")
            return False

        return True

    def RemoveMod(self, ModName: str) -> bool:
        """
        删除mod
        :param ModName: str
        :return: bool
        """
        logger.info(f"从{self.ServerName}中删除{ModName}")
        __path = GetServerPath(self.ServerName)
        if __path is False:
            return False

        __path = ModsDirEvent(__path)
        if __path is False:
            return False

        # 删除mod
        __path = os.path.join(__path, ModName)
        if os.path.isfile(__path) is True:
            try:
                os.remove(__path)
            except Exception as e:
                logger.error(f"从{self.ServerName}中删除{ModName}时出现错误：{e}")
                return False

        return True


def GetServerPath(ServerName: str) -> str or bool:
    """
    获取服务器的完整路径
    :param ServerName: str
    :return: str or bool
    """
    result = os.path.split(os.path.split(__file__)[0])[0]
    result = os.path.join(result, fr"Servers\{ServerName}")
    logger.info(result)
    if os.path.isdir(result) is False:
        logger.error(f"未找到服务器：{ServerName}")
        return False

    return result


def ModsDirEvent(ServerPath: str) -> str or bool:
    """
    判断ServerPath这个目录下是否有mods文件夹，如果有则返回路径，否则返回False
    :param ServerPath:
    :return:
    """
    result = os.path.join(ServerPath, "mods")
    if os.path.isdir(result) is False:
        try:
            os.mkdir(result)
        except Exception as e:
            logger.error(f"创建mods文件夹时出现错误：{e}")
            return False

    return result
