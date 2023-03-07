import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter

findlik = re.compile(r'<a href="(.*?)">')  # 电影链接
daiyingtupians = re.compile(r'<img.*src="(.*?)"', re.S)  # 电影图片

dainyingmingzis = re.compile(r'<span class="title">(.*)</span>')  # 电影名字

# 电影评分
dainyingpingfens = re.compile(
    r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数

dainyingpingjias = re.compile(r'<span>(\d+)人评价</span>')

# 电影详情
dainyingxaingqings = re.compile(r'<span class="inq">(.*)</span>')
# 相关内容
dainyingxiangguans = re.compile(r'<p class="">(.*?)</p>', re.S)
pf = pd.DataFrame(columns=['电影链接', '电影图片', '电影名字',
                  '电影评价人数', '电影评分', '电影详情', '电影内容'])

urls = [
    "https://movie.douban.com/top250?start={}".format(str(i*25)) for i in range(25)]
for url in urls:

    xiangying = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
    }
    # 发送请求，获取响应

    # 返回网页源码

    response = requests.get(url=url, headers=xiangying)
    pf = pd.DataFrame(columns=['电影链接', '电影图片', '电影名字',
                      '电影评价人数', '电影评分', '电影详情', '电影内容'])
# 获取
# print(response.text)
# 解析数据
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("div", class_="item")
    data_list = []
    m = 1
    for result in results:
        result = str(result)
        lianjie = re.findall(findlik, result)[0]  # 链接
        dainyingtupain = re.findall(daiyingtupians, result)[0]  # 图片
        dainyingmingzi = re.findall(dainyingmingzis, result)[0]  # 名字
        dainyingpingjia = re.findall(dainyingpingjias, result)[0]  # 人数
        dainyingpingfen = re.findall(dainyingpingfens, result)[0]  # 评分
        try:
            dainyingxiangqing = re.findall(
                dainyingxaingqings, result)[0]  # 详情
        except IndexError:
            pass
        dainyingxiangguand = re.findall(
            dainyingxiangguans, result)[0]  # 内容
        dainyingxiangguand = dainyingxiangguand.replace("<br/>", "")
        dainyingxiangguand = dainyingxiangguand.strip().replace("\n", "").replace(" ", "")

        print(m, lianjie, dainyingtupain, dainyingmingzi, dainyingpingfen,
              dainyingxiangqing, dainyingxiangguand, dainyingpingjia)

        # print(dainyingxiangguand)
        # 保存数据
        
        pf.loc[len(pf.index)] = [lianjie, dainyingtupain, dainyingmingzi,
                                 dainyingpingjia, dainyingpingfen, dainyingxiangqing, dainyingxiangguand]

        m += 1

pf.to_excel('mmmm.xlsx', sheet_name='mmmm', na_rep="")
"""
        data_dict = {
            '电影链接': lianjie,
            '电影图片': dainyingtupain,
            '电影名字': dainyingmingzi,
            '电影评价人数':dainyingpingjia,
            '电影评分': dainyingpingfen,
            '电影详情': dainyingxiangqing,
            '电影内容': dainyingxiangguand,
        }
        """
"""
            file = open('dict.txt', 'a', encoding='utf-8')
            for key, value in data_dict.items():
                file.write(key + ':' + str(value) + '\n')
            file.close()
            """
# data_list.append(data_dict)
# print(data_dict)

# print(result)
