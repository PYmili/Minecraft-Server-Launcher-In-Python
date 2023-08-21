import os
import subprocess
from abc import ABC, abstractmethod

import requests
from fake_user_agent import user_agent
from lxml import etree


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
        """获取当前可用核心列表"""


class BackendMethod(Action):
    def __init__(self, ser_name: str = 'Test_1.18',
                 xmx: str = '4096',
                 xms: str = '2048',
                 select_v: str = '1.18',
                 new_name: str = 'default',
                 ):
        """
        ser_name:选择启动的服务器名称
        select_v:选择下载的服务器版本
        new_name:新建的服务器名称
        xmx:最大内存
        xms:最小内存
        """
        self.ser_name = ser_name
        self.select_v = select_v
        self.new_name = new_name
        self.spigot_url = f'https://mcversions.net/download/{self.select_v}'
        self.requests_head = {'User-Agent': user_agent()}
        self.xmx = xmx
        self.xms = xms

    def startServer(self) -> None:
        """此函数由启动服务器事件调用"""
        subprocess.Popen(f'java -{self.xmx} -{self.xms} -jar ../Servers/{self.ser_name}/server.jar',
                         shell=True)

    def DownloadJar(self) -> None:
        """此方法由下载事件调用"""
        req = requests.get(url=self.spigot_url, headers=self.requests_head)
        html = etree.HTML(req.text)
        jar_url = html.xpath(f'//a[@download="minecraft_server-{self.select_v}.jar"]/@href')[0]
        jar_req = requests.get(url=jar_url, headers=self.requests_head)
        os.mkdir(rf'../Servers/{self.new_name}_{self.select_v}')
        with open(rf'../Servers/{self.new_name}_{self.select_v}/server.jar', 'ab', encoding='utf-8') as f:
            f.write(jar_req.content)


b = BackendMethod()
b.DownloadJar()
