import re
from bs4 import BeautifulSoup
import requests

DOUBAN_URL = 'https://movie.douban.com/top250'


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    data = requests.get(url, headers=headers).content
    return data


def get_li(data):
    soup = BeautifulSoup(data, 'html.parser')
    ol = soup.find('ol', class_='grid_view')
    name = []  # 名字
    score = []  # 评分
    star_con = []  # 评价人数
    for i in ol.find_all('li'):
        title = i.find('div', class_='hd')
        if title.find('span', class_='title').get_text():
            name.append(title.find('span', class_='title').get_text())

        other_info = i.find('div', class_='bd')
        star_info = other_info.find('div', class_='star')
        if star_info.find('span', class_='rating_num').get_text():
            score.append(star_info.find('span', class_='rating_num').get_text())
        if star_info.find(string=re.compile("评价")).get_text():
            star_con.append(star_info.find(string=re.compile("评价")).get_text())

    paginator = soup.find('span', attrs={'class': 'next'}).find('a')
    if paginator:
        return name, score, star_con, DOUBAN_URL + paginator['href']
    return name, score, star_con, None


def main():
    url = DOUBAN_URL
    total_name = []
    total_score = []
    total_star_con = []
    while url:
        data = download_page(url)
        name, score, star_con, url = get_li(data)
        total_name = total_name + name
        total_score = total_score + score
        total_star_con = total_star_con + star_con

    res = zip(total_name, total_score, total_star_con)
    for i in res:
        print(i)


if __name__ == '__main__':
    main()
