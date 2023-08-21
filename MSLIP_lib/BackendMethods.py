import os
import subprocess

import requests
from fake_user_agent import user_agent
from lxml import etree

from Action import ServerAction


class BackendMethod(ServerAction):
    def __init__(self, ser_name: str = 'Test_1.18',
                 xmx: str = '4096',
                 xms: str = '2048',
                 select_v: str = '1.19',
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
        self.spigot_url = f'https://minecraft.fandom.com/zh/wiki/Java版{self.select_v}'
        self.requests_head = {'User-Agent': user_agent()}  #
        self.xmx = xmx
        self.xms = xms

    def startServer(self) -> None:
        """此函数由启动服务器事件调用"""
        subprocess.Popen(f'java -{self.xmx} -{self.xms} -jar ../Servers/{self.ser_name}/server.jar',
                         shell=True)

    def DownloadJar(self) -> None:
        """此方法由下载事件调用"""
        with requests.get(url=self.spigot_url, headers=self.requests_head) as get:
            html = etree.HTML(get.text)

        jar_url = html.xpath('//tr[5]//a[last()]/@href')[0]
        with requests.get(url=jar_url, headers=self.requests_head, stream=True) as jar_get:
            if jar_get.status_code == 200:
                if os.path.isdir(rf'../Servers/{self.new_name}_{self.select_v}') is False:
                    os.mkdir(rf'../Servers/{self.new_name}_{self.select_v}')
                with open(rf'../Servers/{self.new_name}_{self.select_v}/server.jar', 'wb') as f:
                    for chunk in jar_get.iter_content(8192):
                        f.write(chunk)

    def GetJarList(self) -> list:
        """返回可用版本列表"""
        v_list = []
        server_list = os.listdir(r'../Servers')
        for i in server_list:
            v_list.append(i.split('_')[-1])
        return v_list


# b = BackendMethod()
# b.DownloadJar()
