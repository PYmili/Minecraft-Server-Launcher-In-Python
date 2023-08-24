import os

import requests
from fake_user_agent import user_agent
from lxml import etree
from loguru import logger

from .Action import ServerAction


class BackendMethod(ServerAction):
    def __init__(self, server_name: str = 'Test_1.18',
                 server_version: str = '1.18',
                 ):
        """
        :param server_name: 选择启动的服务器名称
        :param server_version: 选择下载的服务器版本
        """
        self.ServerName = server_name
        self.ServerVersion = server_version
        self.currentFolder = os.path.split(os.path.split(__file__)[0])[0]

        self.official_url = 'https://launcher.mojang.com/v1/objects/'
        self.manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        self.spigot_url = f'https://download.getbukkit.org/spigot/spigot-{self.ServerVersion}.jar'
        self.forge_url = f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{self.ServerVersion}.html'
        self.requests_head = {'User-Agent': user_agent()}

    def auto_change(self):
        with open(fr'./Servers/{self.ServerName}/eula.txt', 'w', encoding='utf-8') as f:
            f.write("""#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
#Tue Aug 22 00:25:11 CST 2023
eula=true""")

    def Download_official(self) -> str:
        """此方法由下载事件调用：下载官方server"""
        logger.info(f'Download_official: {self.ServerVersion}')
        with requests.get(self.manifest_url) as manifest_get:
            if manifest_get.status_code != 200:
                logger.warning("无法获取版本清单。")
                return False
            else:
                manifestJson = manifest_get.json()

        selected_version = None
        for entry in manifestJson["versions"]:
            if entry["id"] == self.ServerVersion:
                selected_version = entry
                break

        if selected_version is None:
            logger.warning("版本无效")
            return False

        with requests.get(selected_version["url"], stream=True) as jar_response:
            if jar_response.status_code != 200:
                logger.warning("无法获取JAR文件。")
                return False

        __path = r'Servers\DownLoads\jar\official_hub'
        __path = os.path.join(self.currentFolder, __path)
        if os.path.isdir(__path) is False:
            try:
                os.mkdir(__path)
            except FileNotFoundError:
                logger.error(f"程序的{__path}文件夹缺失！")

        jar_filename = os.path.join(
            r"Servers\DownLoads\jar\official_hub",
            selected_version["id"] + ".jar"
        )
        with open(jar_filename, "wb") as f:
            for chunk in jar_response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True

    def Download_spigot(self) -> None:
        """此方法由下载事件调用：下载spigot"""
        logger.info(f'Download_forge: {self.ServerVersion}')
        jar_req = requests.get(url=self.spigot_url, headers=self.requests_head)
        os.mkdir(rf'.\Servers\DownLoads\jar\spigot_hub\{self.ServerVersion}')
        with open(rf'.\Servers\DownLoads\jar\spigot_hub\{self.ServerVersion}\server_spigot.jar', 'wb') as f:
            f.write(jar_req.content)

    def Download_forge(self) -> None:
        """此方法由下载事件调用：下载forge"""
        logger.info(f'Download_forge: {self.ServerVersion}')
        req = requests.get(url=self.forge_url, headers=self.requests_head)
        html = etree.HTML(req.text)
        version = html.xpath('//div[@class="title"]/small/text()')[0]
        forge_url = f'https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar'.replace(
            ' ', '')
        logger.info(forge_url)
        jar_req = requests.get(url=forge_url, headers=self.requests_head)
        os.mkdir(rf'.\Servers\DownLoads\Forge\{self.ServerVersion}')
        with open(rf'.\Servers\DownLoads\Forge\{self.ServerVersion}\forge_{self.ServerVersion}.jar', 'wb') as f:
            f.write(jar_req.content)

    def GetJarList(self) -> list:
        """返回可用版本列表"""
        result = []
        for paths, dirs, files in os.walk(r'.\Servers\DownLoads\Jar'):
            for file in files:
                if os.path.splitext(file)[-1] == ".jar":
                    result.append(os.path.join(paths, file))

        return result

    def GetOfficialGameServerList(self) -> list:
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
