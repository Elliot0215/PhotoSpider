#coding=utf-8
__author__ = 'wp'

import re
from lxml import etree
import urllib
import sys
import requests
import logging

class DownPhoto:
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger()
    handler = logging.FileHandler("../../../log.txt")
    log.addHandler(handler)

    def __init__(self,host):
        self.host = host

    @staticmethod
    def formatUrl(innerUrl,index):
        listUrl =list(str(innerUrl))
        listUrl.insert(-5,"_"+str(index))
        photoPageUrl = ''.join(listUrl)
        return photoPageUrl

    @staticmethod
    def filter(dataList):
        new_data = []
        for data in dataList:
            if data.startswith('http'):
                new_data.append(data)
        return new_data

    def downLoad(self):
        self.log.info("############# start download ############")
        self.startPage()
        self.log.info("############# download over ############")

    def startPage(self):
        pageList = ["/meinvtag27736_{}.html".format(i) for i in range(1,6)]
        url = self.host + pageList[1]   #只取了一页
        response = requests.get(url)
        xml = etree.HTML(response.text)
        hrefList = xml.xpath("///div[@class='tab_box']/div/ul/li/a/@href")
        for innerUrl in self.filter(hrefList):
            self.innerPage(innerUrl)

    def innerPage(self,innerUrl):
        response = requests.get(innerUrl)
        number = re.findall("</span>/<em>(\d+)</em>",response.text)[0]
        for index in range(1,int(number)+1):
            self.photoPage(self.formatUrl(innerUrl,index))

    def photoPage(self,photoPageUrl):
        response = requests.get(photoPageUrl)
        imageUrl = re.findall('data-original="(.*?)" url',response.text)[0]
        self.log.info("start download "+imageUrl)
        self.save(imageUrl)

    def save(self,imageUrl):
        try:
            #urllib.urlretrieve(imageUrl,"C:\Users\Administrator\Desktop\image\{}".format(str(imageUrl).split('/')[-1]))   # 调用api的方式
            result = requests.get(imageUrl, stream=True)
            with open('../../../imgs/{}'.format(str(imageUrl).split('/')[-1]), 'wb') as f:
                for buff in result.iter_content(1024):
                    f.write(buff)
        except Exception,msg:
            self.log.error(msg)
            sys.exit(0)



if __name__ == "__main__":
    dp = DownPhoto('http://www.win4000.com')
    dp.downLoad()


