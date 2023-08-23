import os

import requests
from fake_user_agent import user_agent
from lxml import etree

from .Action import ServerAction


class BackendMethod(ServerAction):
    def __init__(self, ser_name: str = 'Test_1.18',
                 select_v: str = '1.18',
                 ):
        """
        ser_name:选择启动的服务器名称
        select_v:选择下载的服务器版本
        """
        self.ser_name = ser_name
        self.select_v = select_v
        self.official_url = f'https://minecraft.fandom.com/zh/wiki/Java版{self.select_v}'
        self.spigot_url = f'https://download.getbukkit.org/spigot/spigot-{self.select_v}.jar'
        self.requests_head = {'User-Agent': user_agent()}

    def auto_change(self):
        with open(fr'./Servers/{self.ser_name}/eula.txt', 'w', encoding='utf-8') as f:
            f.write("""#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
#Tue Aug 22 00:25:11 CST 2023
eula=true""")

    def DownloadJar_official(self) -> None:
        """此方法由下载事件调用"""
        print('DownloadJar_official')
        print(self.select_v)
        req = requests.get(url=self.official_url, headers=self.requests_head)
        html = etree.HTML(req.text)
        jar_url = html.xpath('//a[text()="服务端"]/@href')[0]
        jar_req = requests.get(url=jar_url, headers=self.requests_head)
        os.mkdir(rf'.\DownLoads\jar\official_hub\{self.select_v}')
        with open(rf'.\DownLoads\jar\official_hub\{self.select_v}\server_official.jar', 'wb') as f:
            f.write(jar_req.content)

    def DownloadJar_spigot(self) -> None:
        """此方法由下载事件调用"""
        print('DownloadJar_spigot')
        print(self.select_v)
        jar_req = requests.get(url=self.spigot_url, headers=self.requests_head)
        os.mkdir(rf'.\DownLoads\jar\spigot_hub\{self.select_v}')
        with open(rf'.\DownLoads\jar\spigot_hub\{self.select_v}\server_spigot.jar', 'wb') as f:
            f.write(jar_req.content)

    def GetJarList(self) -> list:
        """返回可用版本列表"""
        result = []
        for paths, dirs, files in os.walk(r'.\DownLoads\Jar'):
            for file in files:
                if os.path.splitext(file)[-1] == ".jar":
                    result.append(os.path.join(paths, file))
                print(result)

        return result
