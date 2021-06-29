import requests
import time
import re
from bs4 import BeautifulSoup


HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }


def parse_ozon(URL):
    parsed_list = []
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find('div', {"class": "container b6e3"})
    k=0
    for i in items:
        if k == 1:
            item = i.find('h1', {"class": "b3a8"})
            parsed_list.append(item.text)
            art = i.find('span', {"class": "b2d7 b2d9"}).text
            otz = i.find('a', {"class": "_1-6r _3UDF"})
            k_otz = otz.find('div', {"class": "kxa6"}).text
            parsed_list.append(art)
            parsed_list.append(k_otz.replace(u'\xa0', u' '))
            k += 1
        elif k == 2:
            item = i.find('div', {"class": "b5y", 'style': 'max-width:370px;flex-basis:370px;'})
            k += 1
        else:
            k += 1
    items = items.find_all('div', {"class": "bo3"})
    k = 0
    for i in items:
        if k == 1:
            k += 1
            item = i.find('span', {"class": "c2h5 c2h6"}).find('span')
            text = item.text
            text = text.replace(u'\xa0', u' ')
            parsed_list.append(text)
        else:
            k += 1
    items = soup.find('a', {"class": "_1-6r _3UDF"})['href']
    rev = ozon_rev('https://www.ozon.ru' + items)
    return parsed_list, rev


def ozon_rev(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all('div', {"class": "d9g7"})
    rev_list = []
    for i in items:
        otz = {}
        name = i.find('span', {"class": "a6x9"}).text
        otz["Name"] = name
        r = i.find_all('span', {"class": "a5a9"})
        coment = ''
        stars = i.find('div', {"class": "_3xol"})['style'][6:9]
        if stars == '104':
            otz["Mark"] = 5
        elif stars == '83.':
            otz["Mark"] = 4
        elif stars == '62.':
            otz["Mark"] = 3
        elif stars == '41.':
            otz["Mark"] = 2
        else:
            otz["Mark"] = 1
        for j in r:
            coment += j.text
        otz["Com"] = coment.replace(u'\xa0', u' ')
        rev_list.append(otz)

    return rev_list


def parse_wb(URL):
    urlm = (URL.split('/'))
    urlm = urlm[:5]
    URL = ''
    for i in urlm:
        URL += i + '/'
    URL += 'otzyvy'
    parsed_list = []
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find('div', {"class": "main__container"})
    name = items.find('meta', {"itemprop": "name"})
    parsed_list.append(name['content'])
    item = items.find('div', {"class": "second-horizontal"})
    art = items.find('div', {"class": "article"})
    parsed_list.append(art.find('span').text)
    otz = item.find('i')
    parsed_list.append(otz.text.replace(u'\n', u''))
    price = items.find('meta', {"itemprop": "price"})['content']
    parsed_list.append(price)
    comentb = items.find('div', {"class": "comments"})
    coments = comentb.find_all('div', {"class": "comment j-b-comment"})
    rev_list = []
    for com in coments:
        otz = {}
        otz["Name"] = com.find('div', {"class": "author"}).text.replace(u'\n', u'')
        stars = com.find('div', {"itemprop": "ratingValue"}).text
        otz["Mark"] = stars
        otz["Com"] = com.find('p', {"itemprop": "reviewBody"}).text
        rev_list.append(otz)
    return parsed_list, rev_list


def switch(link):
    s = link[12:]
    if s[0] == 'w':
        return parse_wb(link)
    else:
        return parse_ozon(link)

if __name__ == "__main__":
    print(switch('https://www.wildberries.ru/catalog/16023993/detail.aspx?targetUrl=XS'))
    print(' ')
    print(switch('https://www.wildberries.ru/catalog/8329114/detail.aspx'))
    print(' ')
    print(switch('https://www.ozon.ru/product/gornyy-velosiped-rush-hour-rx-905-29-2021-228058566/'))
    print(' ')
    print(switch('https://www.ozon.ru/product/stiralnyy-poroshok-ariel-automat-gornyy-rodnik-12-kg-146781707/?advert=nnCvZ5mOIHxZzRb5FsWWD6VOx4_lDpxyQBzX-orav4GuHvsSK89cr08roPHvz3pnWSwy-NxMmMBsgQGRs3OIPqzKcyhJqIEyRwJO2SsZHedUihWUJqF0Sg1PXobZgwMld9ShALgTI0eIORL0FuXW1mU1kg&hs=1'))
