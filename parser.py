# -*- coding: utf-8 -*-
import requests
import time
import re
from bs4 import BeautifulSoup
import config
import json


HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }


def parse_ozon(URL):
    parsed = {}
    parsed['url'] = URL
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find('div', {"class": "container e0x"})
    k=0
    for i in items:
        if k == 1:
            item = i.find('h1', {"class": "b3a8"})
            parsed['Name'] = item.text
            art1 = i.find('span', {"class": "b2d7 b2d9"}).text
            otz = i.find('a', {"class": "_1-6r _3UDF"})
            k_otz1 = otz.find('div', {"class": "kxa6"}).text
            art = ''
            for symb in art1:
                if symb >= '0' and symb <= '9':
                    art = art + symb
            parsed['Art'] = art
            k_otz = ''
            for symb in k_otz1:
                if symb >= '0' and symb <= '9':
                    k_otz = k_otz + symb
            parsed['Col_otz'] = k_otz
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
            price = ''
            for symb in text:
                if symb >= '0' and symb <= '9':
                    price = price + symb
            parsed['Price'] = price
        else:
            k += 1
    items = soup.find('a', {"class": "_1-6r _3UDF"})['href']
    rev = ozon_rev('https://www.ozon.ru' + items)
    return parsed, rev


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
    parsed = {}
    parsed['url'] = URL
    urlm = (URL.split('/'))
    urlm = urlm[:5]
    URL = ''
    for i in urlm:
        URL += i + '/'
    URL += 'otzyvy'
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find('div', {"class": "main__container"})
    name = items.find('meta', {"itemprop": "name"})
    parsed['Name'] = name['content']
    item = items.find('div', {"class": "same-part-kt__common-info"})
    art = items.find('p', {"class": "same-part-kt__article"})
    articul = art.find('span', {"data-link": "text{: selectedNomenclature^cod1S}"})
    parsed["Art"] = articul.text
    otz = item.find('span', {"data-link": "{include tmpl='productCardCommentsCount'}"}).text
    k_otz = ''
    for symb in otz:
        if symb >= '0' and symb <= '9':
            k_otz = k_otz + symb
    parsed['Col_otz'] = k_otz
    price = items.find('span', {"class": "price-block__final-price"})
    if price is not None:
        price = price.text
        final_price = ''
        for symb in price:
            if symb >= '0' and symb <= '9':
                final_price = final_price + symb
        parsed["Price"] = final_price
    else:
        parsed["Price"] = '0'
    comentb = items.find('div', {"class": "comments"})
    coments = comentb.find_all('li', {"class": "comments__item feedback"})
    rev_list = []
    for com in coments:
        otz = {}
        otz["Name"] = com.find('a', {"class": "feedback__header"}).text.replace(u'\n', u'')
        stars = com.find('span', {"itemprop": "reviewRating"})['class']
        otz["Mark"] = stars[1][4:]
        otz["Com"] = com.find('p', {"class": "feedback__text"}).text
        rev_list.append(otz)
    return parsed, rev_list


def switch(link):
    s = link[12:]
    if s[0] == 'w':
        return parse_wb(link)
    else:
        return parse_ozon(link)

if __name__ == "__main__":
    while True:
        answer = requests.get(config.url + '/links/parse/', data=json.dumps({}), verify=False).json()
        print(answer, 'get')
        for i in answer:
            try:
                a = switch(i['link'])
                answer = requests.put(config.url + 'links/update/', data=json.dumps(a), verify=False)
                print(answer, 'put')
            except Exception as e:
                print('parse link err:', i['link'])
        time.sleep(config.delay)