import requests

weather_api_key = "e9d7239a61fade4678c26fe1059913d3"

city = "Taganrog"

url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&lang=ru'

res = requests.get(url)
data = res.json()

for forecast in data['list']:
    print(f"Время: {forecast['dt_txt']}, Температура воздуха: {round(forecast['main']['temp'] - 273, 1)} °C, Скорость ветра: {round(forecast['wind']['speed'], 2)} м/с, Давление: {round(forecast['main']['pressure'] * 0.75)} мм рт. ст., Влажность: {forecast['main']['humidity']} %, Погода: {forecast['weather'][0]['description']}\n\n")
