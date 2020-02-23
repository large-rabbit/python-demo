"""
通过天行数据的API，获取图片url，再多线程下载这些图片

Author: large-rabbit
Version: 1.0
"""
import requests
from threading import Thread


class Download(Thread):
    """
    构造多线程类
    """
    def __init__(self, url):
        """
        初始化类
        :param url: 图片url
        """
        super().__init__()
        self._url = url

    def run(self):
        file_name = self._url[self._url.rfind('/') + 1:]
        r = requests.get(self._url)
        with open('C:\\Users\\28602\\Desktop\\test\\' + file_name, 'wb') as f:
            f.write(r.content)


def get_data():
    """
    获取图片url
    :return: 包含图片url的字典
    """
    url = 'http://api.tianapi.com/meinv/index'
    params = {'key': 'key', 'num': '10'}
    r = requests.get(url, params=params)
    return r.json()


def main():
    data = get_data()
    tasks = []
    for picurl in data['newslist']:
        task = Download(picurl['picUrl'])
        tasks.append(task)
        task.start()
    for task in tasks:
        task.join()
    print('下载完成')


if __name__ == '__main__':
    main()
