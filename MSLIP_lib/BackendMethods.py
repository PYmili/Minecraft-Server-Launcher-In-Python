import os
import subprocess

import requests
from fake_user_agent import user_agent
from lxml import etree

from Action import ServerAction


class BackendMethod(ServerAction):
    def __init__(self, ser_name: str = 'Test_1.18',
                 xmx: str = '2',
                 xms: str = '1',
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

    def startServer(self) -> subprocess.Popen:
        """此函数由启动服务器事件调用"""
        path = os.path.dirname(os.path.realpath(__file__))[:-10] + f'/Servers/{self.ser_name}/server.jar'
        print(f'cd../Servers/{self.ser_name} && java -Xmx{self.xmx}g -Xms{self.xms}g -jar {path}')
        server_process = subprocess.Popen(
            fr'cd../Servers/{self.ser_name} && java -Xmx{self.xmx}g -Xms{self.xms}g -jar {path}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        print('ok')
        return server_process

    def DownloadJar(self) -> None:
        """此方法由下载事件调用"""
        req = requests.get(url=self.spigot_url, headers=self.requests_head)
        html = etree.HTML(req.text)
        jar_url = html.xpath('//tr[5]//a[last()]/@href')[0]
        jar_req = requests.get(url=jar_url, headers=self.requests_head)
        os.mkdir(rf'../Servers/{self.new_name}_{self.select_v}')
        with open(rf'../Servers/{self.new_name}_{self.select_v}/server.jar', 'wb') as f:
            f.write(jar_req.content)

    def GetJarList(self) -> list:
        """返回可用版本列表"""
        v_list = []
        server_list = os.listdir(r'../Servers')
        for i in server_list:
            v_list.append(i.split('_')[-1])
        return v_list


# b = BackendMethod()
# b.DownloadJar()
