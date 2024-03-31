import requests
import time

city = 'Taganrog'
match_date = "31.03.2024 16:30"
unix_match_date = int(time.mktime(time.strptime(match_date, '%d.%m.%Y %H:%M')))
# print(unix_match_date)
# print(int(time.time() // 1))

weather_api_key = "e9d7239a61fade4678c26fe1059913d3"
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric&lang=ru'
res = requests.get(url)
data = res.json()

if (unix_match_date - int(time.time() // 1) <= 3600*3) and (unix_match_date - int(time.time() // 1) > 0):
    for forecast in data['list']:
        # if forecast['dt'] - unix_match_date <= 3600*3:
        #     print(f"Время: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'])} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n")
        # elif forecast['dt'] - unix_match_date >= 3600*3 and forecast['dt'] - unix_match_date <= 3600*5:
        #     print(f"Время: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'])} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n")
        # else:
        #     pass
        print(f"Время: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'])} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n")
else:
    pass
