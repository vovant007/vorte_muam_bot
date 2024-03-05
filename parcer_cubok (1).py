import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def parcer__cubok():


    url = 'https://soccer365.ru/competitions/786/'
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"
    }
    req = requests.get(url, headers)
    src = req.text
    with open("index_cubok.html", "w", encoding='utf-8') as file:
        file.write(src)
    with open("index_cubok.html", encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_products_hrefs = soup.find_all('span', class_="tabs_item")
    a = []
    all_categories_dict = {}
    for i in all_products_hrefs:
        a.append(i.find('a'))
    for item in a:
        if item is not None:
            item_text = item.text
            item_href = 'https://soccer365.ru/competitions/786/' + item.get("href")
            all_categories_dict[item_text] = item_href
    with open("all_categories_dict.json", "w") as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    with open("all_categories_dict.json") as file:
        all_categories = json.load(file)

    url_raspis = all_categories.setdefault('Расписание')
    req_raspis = requests.get(url_raspis, headers=headers)
    src_raspis = req_raspis.text
    with open("index_cubok2.html", "w", encoding='utf-8') as file:
        file.write(src_raspis)
    soup = BeautifulSoup(src_raspis, "lxml")
    table=soup.find_all('div',class_='live_comptt_bd')
    table_name=[]
    for i in table:
        table_name.append(i.find_all('div',class_='cmp_stg_ttl'))
    table_name_text=[]
    #-загаловок
    for i in table_name:
        for j in i:
            table_name_text.append(j.text)

    table_game=[]
    for i in table:
        table_game.append(i.find_all('div',class_='block_body_nopadding'))
    table_game_=[]
    for i in table_game:
        for j in i:
            table_game_.append(j.find_all('div',class_='game_block'))
    table_game__=[]
    for i in table_game_:
        for j in i:
            table_game__.append(j.find_all('a',class_='game_link'))
    table_game__data=[]
    for i in table_game__:
        for j in i:
            table_game__data.append(j.find_all('div',class_='status'))
     #-дата
    table_game__data_text=[]
    for i in table_game__data:
        for j in i:
            table_game__data_text.append(j.text)

    table_game__result=[]
    for i in table_game__:
        for j in i:
            table_game__result.append(j.find_all('div',class_='result'))

    #-левая команда
    table_game__result__ht=[]
    for i in table_game__result:
        for j in i:
            table_game__result__ht.append(j.find_all('div',class_='ht'))
    table_game__result__ht__name=[]
    for i in table_game__result__ht:
        for j in i:
            table_game__result__ht__name.append(j.find_all('div',class_='name'))
    table_game__result__ht__name_text=[]
    for i in table_game__result__ht__name:
        for j in i:
            table_game__result__ht__name_text.append(j.text)
    #-правая команда
    table_game__result__at = []
    for i in table_game__result:
        for j in i:
            table_game__result__at.append(j.find_all('div', class_='at'))
    table_game__result__at__name = []
    for i in table_game__result__at:
        for j in i:
            table_game__result__at__name.append(j.find_all('div', class_='name'))
    table_game__result__at__name_text = []
    for i in table_game__result__at__name:
        for j in i:
            table_game__result__at__name_text.append(j.text)
    try:
        new_list_cubok = [
            f"{table_game__data_text[i]}: {table_game__result__ht__name_text[i]}-{table_game__result__at__name_text[i]}: {table_name_text[0]}"
            for i in
            range(5)]
        new_list_cubok+= [
            f"{table_game__data_text[i+5]}: {table_game__result__ht__name_text[i+5]}-{table_game__result__at__name_text[i+5]}: {table_name_text[1]}"
            for i in
            range(8)]
        new_list_cubok += [
            f"{table_game__data_text[i + 13]}: {table_game__result__ht__name_text[i + 13]}-{table_game__result__at__name_text[i + 13]}: {table_name_text[2]}"
            for i in
            range(8)]
    except:
        print('Ошибка формирования  расписания Кубка')
    forte_cubok = []
    for i in new_list_cubok:
        if 'Форте Таганрог' in i:
            forte_cubok.append(i)
    return forte_cubok

def turs_cubok(n):
    forte_cubok=parcer__cubok()
    s=''
    try:
        for i in range(n):
            s += forte_cubok[i] + '\n'
        return s
    except:
        return 'Невозможное кол-во туров'


def date_cubok():
    try:
        c = 0
        forte = parcer__cubok()
        s = forte[c]
        input_date_str = s[:12]
        now = datetime.now()
        input_date = datetime.strptime(input_date_str + f".{now.year}", "%d.%m, %H:%M.%Y")
        diff = input_date - now
        if diff.seconds > 0:
            return f"До ближайшего матча осталось: {diff.days} д., {diff.seconds // 3600} ч., {diff.seconds // 60 % 60} м."
        else:
            c += 1
    except:
        print('Ошибка формирования даты начала ближайшего кубка ')
