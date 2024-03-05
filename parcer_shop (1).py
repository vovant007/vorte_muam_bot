import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def parcer__shop():

    url = 'https://fc-forte.ru/s/'
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"
    }
    req = requests.get(url, headers)
    src = req.text
    with open("index_shop.html", "w", encoding='utf-8') as file:
        file.write(src)
    with open("index_shop.html", encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_products_hrefs = soup.find_all('div', class_="submenu")
    a = []
    all_categories_dict = {}
    for i in all_products_hrefs:
        a.append(i.find_all('a'))
    for item in a:
        for i in item:
            if i is not None and i.get("href"):
                i_text = i.text
                i_href = 'https://fc-forte.ru'+i.get("href")
                all_categories_dict[i_text] = i_href
    return all_categories_dict

def title_text():
    text = []
    for keys in parcer__shop().keys():
        text.append(keys)
    return text
def link_text():
    links=[]
    for value in parcer__shop().values():
        links.append(value)
    return links


def parcer_links(n):
    url = link_text()[n]
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"
    }
    req = requests.get(url, headers)
    src = req.text
    with open(f"{str(n)}.html", "w", encoding='utf-8') as file:
        file.write(src)
    with open(f"{str(n)}.html", encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    product_list=soup.find_all('li',class_='products-list-item')
    print(product_list)
    url=[]
    #url-картинок
    for i in product_list:
        url.append(i.find_all('div',class_='img-wrapper'))
    img=[]
    for i in url:
        for j in i:
            img.append(j.find_all('img'))
    img_url=[]
    for i in img:
        for j in i:
            s='https://fc-forte.ru'+j.get('src')
            img_url.append(s)
    #заголовок
    name=[]
    for i in product_list:
        name.append(i.find_all('h4'))
    name_text=[]
    for i in name:
        for j in i:
            name_text.append(j.text)
    name_text = [item.replace('\n', '').strip() for item in name_text]
    #цена
    price=[]
    for i in product_list:
        price.append(i.find_all('p', class_='price'))
    price_val=[]
    for i in price:
        for j in i:
            price_val.append(j.find_all( class_='old-price val'))
    price_old_val_text=[]
    for i in price_val:
        for j in i:
                price_old_val_text.append(j)
    for i in price:
        for j in i:
            price_val.append(j.find_all( class_='val'))
    price_val_text=[]
    for i in price_val:
        for j in i:
                price_val_text.append(j)
    for i in price_old_val_text:
        for j in price_val_text:
            if i==j:
                price_val_text.remove(j)
    price_val_text_=[]
    for i in price_val_text:
        price_val_text_.append(i.text)
    # валюта
    currency=[]
    for i in price:
        for j in i :
            currency.append(j.find_all(class_='currency'))
    currency_text=[]
    for i in currency:
        for j in i :
            currency_text.append(j.text)
    title=[]
    for i in range(len(name_text)):
        title.append(f'{name_text[i]} :{price_val_text_[i]}{currency_text[i]}')
    return img_url,name_text







