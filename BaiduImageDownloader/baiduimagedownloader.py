# -*- encoding:utf-8 -*-

import urllib.parse
import urllib.request
import os
import re
from threading import *

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e',
    'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j',
    'h': 'k', 's': 'l', '4': 'm', 'g': 'n', '5': 'o',
    'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't',
    '7': 'u', 'e': 'v', 'o': 'w', '8': '1', 'd': '2',
    'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7',
    'b': '8', 'l': '9', 'a': '0'
}


def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)

    l = list(url)

    for i in range(len(l)):
        if l[i] in char_table.keys():
                l[i] = char_table[l[i]]


    return "".join(l)

def request(url, header):
    rep = urllib.request.Request(url, headers=header)
    rep = urllib.request.urlopen(rep)
    try:
        html = rep.read().decode('utf-8')
        return html
    except:
        print("something wrong!")
    return None

class BaiduImageDownloader:

    def __init__(self, search_word, directory):
        self.__word = urllib.parse.quote(search_word, 'utf-8')
        self.directory = directory
        self.__index_header = {
                    "Accept": "text/plain, */*; q=0.01",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Connection": "keep-alive",
                    "Cookie": "BDqhfp=test%26%260-10-1undefined%26%260%26%261; winWH=%5E6_1476x855; BDI"
                              "MGISLOGIN=0; AIDUID=A03A6D818A8FBC04E0DEFFEF80DAAE17:FG=1; BIDUPSID=A03A"
                              "6D818A8FBC04E0DEFFEF80DAAE17; PSTM=1477565017; __cfduid=d26a2d5b814b377b"
                              "04c67bcb39ad5ef051477565021; MCITY=-31080%3A218%3A; indexPageSugList=%5B"
                              "%22%E5%A3%81%E7%BA%B8%22%2C%22test%22%2C%22123%22%2C%22cat%22%2C%22%E5%A3"
                              "%81%E7%BA%B8%E6%B7%B1%E6%B5%B7%22%2C%22%E5%8A%A8%E6%BC%AB%22%5D; H_PS_PSS"
                              "ID=1436_21079; PSINO=3; pgv_pvi=4535854080; pgv_si=s5365098496; BDRCVFR[-"
                              "pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[X_XKQks"
                              "0S63]=mk3SLVN4HKm; firstShowTip=1; cleanHistoryStatus=0; userFrom=null",
                    "Host": "image.baidu.com",
                    "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm="
                               "-1&st=-1&fm=result&fr=&sf=1&fmq=1499929773360_R&pv=&ic=0&nc=1&z=&se=1&showtab"
                               "=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&"
                               "word={search_word}".format(search_word=self.__word),
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
                    "X-Requested-With": "XMLHttpRequest"
                }


        self.__url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=20132659" \
                     "2&is=&fp=result&queryWord="+self.__word+"&cl=2&lm=-1&ie=utf-8&oe=utf-8&a" \
                     "dpicid=&st=-1&z=&ic=0&word="+self.__word+"&s=&se=&tab=&width=&height=&fa" \
                     "ce=0&istype=2&qc=&nc=1&fr=&cg=girl&pn={page_num}&rn=30&gsm=1e&14999" \
                     "30222917="


        self.__stop = False


    def __get_index_url(self):
        return "https://image.baidu.com/search/index?tn=baidu" \
               "image&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=i" \
               "ndex&fr=&hs=0&xthttps=111121&sf=1&fm" \
               "q=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&i" \
               "stype=2&ie=utf-8&word={search_word}".format(search_word=str(self.word))



    def download_core(self):
        i = 0
        index = 0
        while True:
            if self.__stop:
                return None
            i += 1
            url = self.__url.format(page_num=str(i*30))
            html = request(url, self.__index_header)
            if html is None:
                continue

            finds = re.compile('objURL":".*?"').findall(html)
            for f in finds:
                if self.__stop:
                    return None
                f = f.replace('objURL":"', '').replace('"', '')
                u = decode(f)
                if self.__save_file(u, str(index)+'.jpg'):
                    index += 1



    def stop_download(self):
        self.__stop = True


    def __save_file(self, url, fn):
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

        try:
            urllib.request.urlretrieve(url, self.directory+"\\"+fn)
            print("download:", url, "\tcompleted")
            return True
        except:
            print("download:", url, "\t failed")

        return False


def detect_key(downloader):
    l = ['q', 'Q']

    while True:
        k = input()
        if k in l:
            downloader.stop_download()
            print('正在停止下载...')
            break

if __name__ == '__main__':
    word = input("输入搜索关键字：")
    path = input("输入存储路径：")
    dn = BaiduImageDownloader(word, path)
    Thread(target=dn.download_core).start()
    detect_key(dn)
