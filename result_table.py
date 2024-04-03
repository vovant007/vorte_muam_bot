import requests
from bs4 import BeautifulSoup
import json
def table():
    url = 'https://soccer365.ru/competitions/2205/'
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"}
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
    url_raspis = all_categories_dict.setdefault('Турнир')
    req_raspis = requests.get(url_raspis, headers=headers)
    src_raspis = req_raspis.text
    soup = BeautifulSoup(src_raspis, "lxml")
    general = soup.find('table', class_='stngs')
    title = general.find_all('tr', class_='stngs_hdr')
    title_name = []
    for i in title:
        title_name.append(i.find_all('th', class_='ctr'))
    title_name_text = []
    for i in title_name:
        for j in i:
            title_name_text.append(j.text)

    row_data = []
    for row in general.find_all('tr'):  # Обход строк таблицы
        cells = row.find_all('td')  # Находим все ячейки в текущей строке
        for cell in cells:
            row_data.append(cell.text.strip())
    row_data_right = []
    data_str = ' | '.join(row_data[0:10])
    for i in row_data:
        row_data_right.append(i)
        row_data_right.append('|')
    sublists = [row_data_right[i:i + 20] for i in range(0, len(row_data_right), 20)]
    result_list = [''.join(sublist) for sublist in sublists]
    title_name_text.insert(0, 'М')
    title_name_text.insert(1, 'Команда')
    data_name_text_right = '|'.join(map(str, title_name_text))
    s = ''
    s += data_name_text_right + '\n'
    for i in result_list:
        s += i + '\n'
    return s
