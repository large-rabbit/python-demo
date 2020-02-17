import requests
from bs4 import BeautifulSoup
import bs4


def GetHTMLText(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def FillList(html, videoList):
    soup = BeautifulSoup(html, "html.parser")
    for li in soup.find("ul", "rank-list").children:
        rank = li.find("div", "num").string
        name = li.find("div", "info").a.string
        link = li.find("div", "info").a.attrs["href"]
        pop = li.find("i", "b-icon play").next_sibling.string
        up = li.find("i", "b-icon author").next_sibling.string
        info = {"rank": rank, "name": name, "link": "http:"+link, "pop": pop, "up": up}
        videoList.append(info)


def PrintList(videoList, num, status):
    tem = ""
    if status == "basic":
        print("Bilibili播放排行榜（基本版）:")
        tem = "排名：{0}\n视频名：{1}\n"
    elif status == "all":
        print("Bilibili播放排行榜（完整版）：")
        tem = "排名：{0}\n视频名：{1}\n链接：{2}\t人气：{3}\tup主：{4}\n"
    for n in range(num):
        info = videoList[n]
        print(tem.format(info["rank"], info["name"], info["link"], info["pop"], info["up"]))


if __name__ == "__main__":
    url = "https://www.bilibili.com/ranking"
    num = 20
    videoList=[]
    try:
        html = GetHTMLText(url)
        FillList(html, videoList)
        PrintList(videoList, 20, "all")
    except requests.exceptions.HTTPError as e:
        print("访问错误！")
