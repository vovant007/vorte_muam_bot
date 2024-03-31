import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

#Переменные для погоды
weather_api_key = "e9d7239a61fade4678c26fe1059913d3"
city = "Taganrog"
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric&lang=ru'
res = requests.get(url)
data = res.json()

def parcer():
    url = 'https://soccer365.ru/competitions/2205/'
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"
    }
    req = requests.get(url, headers)
    src = req.text
    with open("index.html", "w", encoding='utf-8') as file:
        file.write(src)
    with open("index.html", encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_hrefs = soup.find_all('span', class_="tabs_item")
    a = []
    all_categories_dict = {}
    for i in all_hrefs:
        a.append(i.find('a'))
        for item in a:
            if item is not None:
                item_text = item.text
                item_href = "https://soccer365.ru/competitions/2205/" + item.get("href")
                all_categories_dict[item_text] = item_href
    with open("all_categories_dict.json", "w", encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    with open("all_categories_dict.json", encoding='utf-8') as file:
        all_categories = json.load(file)

    url_raspis = all_categories_dict.setdefault('Расписание')
    req_raspis = requests.get(url_raspis, headers=headers)
    src_raspis = req_raspis.text
    soup = BeautifulSoup(src_raspis, "lxml")
    table = soup.find_all('div', class_='live_comptt_bd')
    table_name = []
    for i in table:
        table_name.append(i.find_all('div', class_='cmp_stg_ttl'))
    table_name_text = []
    # -загаловок
    table_game = []
    for i in table_name:
        for j in i:
            table_name_text.append(j.text)
    for i in table:
        table_game.append(i.find_all('div', class_='block_body_nopadding'))
    table_game_ = []
    for i in table_game:
        for j in i:
            table_game_.append(j.find_all('div', class_='game_block'))
    table_game__ = []
    for i in table_game_:
        for j in i:
            table_game__.append(j.find_all('a', class_='game_link'))
    table_game__data = []
    for i in table_game__:
        for j in i:
            table_game__data.append(j.find_all('div', class_='status'))
    # -дата
    table_game__data_text = []
    for i in table_game__data:
        for j in i:
            table_game__data_text.append(j.text)
    table_game__result = []  # Линия результата матча
    for i in table_game__:
        for j in i:
            table_game__result.append(j.find_all('div', class_='result'))
    # -левая команда
    table_game__result__ht = []
    for i in table_game__result:
        for j in i:
            table_game__result__ht.append(j.find_all('div', class_='ht'))
    table_game__result__ht__name = []
    for i in table_game__result__ht:  # класс левой команды
        for j in i:
            table_game__result__ht__name.append(j.find_all('div', class_='name'))

    table_game__result__ht__name_text = []  # Список левых команд
    for i in table_game__result__ht__name:
        for j in i:
            table_game__result__ht__name_text.append(j.text)
    # -правая команда
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
        new_list = [
            f"{table_game__data_text[i]}: {table_game__result__ht__name_text[i]}-{table_game__result__at__name_text[i]} "
            for i in
            range(len(table_game__data_text))]
    except:
        print('Ошибка формирования')
    forte=[]
    for i in new_list:
        if 'Форте Таганрог' in i:
            forte.append(i)
    return forte


def right_forte():
    forte = parcer()
    forte_new = []
    for i in forte:
        input_date_str = i[:12]
        now = datetime.now()
        input_date = datetime.strptime(input_date_str + f".{now.year}", "%d.%m, %H:%M.%Y")
        diff = input_date - now
        if diff.total_seconds() > 0:
            forte_new.append(i)
    return forte_new


def turs(n):
    forte=right_forte()
    s=''
    try:
        for i in range(n):
            s += forte[i] + '\n'
        return s
    except:
        return 'Невозможное кол-во туров'


def date():
    forte=right_forte()
    s=forte[0]
    input_date_str=s[:12]
    now = datetime.now()
    input_date = datetime.strptime(input_date_str + f".{now.year}", "%d.%m, %H:%M.%Y")
    diff = input_date - now
    return f"До ближайшего матча осталось: {diff.days} д., {diff.seconds // 3600} ч., {diff.seconds // 60 % 60} м.", input_date

def weather():
    input_date = date()[1]
    input_date = int(time.mktime(time.strptime(str(input_date), '%Y-%m-%d %H:%M:%S')))
    d = right_forte()
    if (input_date - int(time.time() // 1) <= 3600*3) and (input_date - int(time.time() // 1) > 0):
        for forecast in data['list']:
            if forecast['dt'] - input_date <= 3600*3:
                d[0] = d[0] + f"\nВремя: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'])} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n"
            elif forecast['dt'] - input_date >= 3600*3 and forecast['dt'] - input_date <= 3600*5:
                d[0] = d[0] + f"\nВремя: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'])} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n"
            else:
                pass
    else:
        pass
    return d
