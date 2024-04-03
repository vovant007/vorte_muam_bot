import vk_api
from bot_token import vk_token
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from  pars_games_new_with_weather import date,turs
import requests
from parcer_shop import parcer__shop
from rand_line import facts
from result_table import table

session = vk_api.VkApi(token=vk_token)
bot_api = session.get_api()


def send_photo(user_id, url):
    upload_url = session.method("photos.getMessagesUploadServer", {"peer_id": user_id})["upload_url"]

    response = requests.get(url)
    files = {
        "photo": ("photo.jpg", response.content)
    }

    response = requests.post(upload_url, files=files)
    json_response = response.json()

    photo = json_response["photo"]
    server = json_response["server"]
    hash = json_response["hash"]

    save_response = session.method("photos.saveMessagesPhoto", {
        "photo": photo,
        "server": server,
        "hash": hash
    })

    photo_data = save_response[0]
    owner_id = photo_data["owner_id"]
    photo_id = photo_data["id"]

    attachment = f"photo{owner_id}_{photo_id}"

    session.method("messages.send", {
        "user_id": user_id,
        "attachment": attachment,
        "random_id": 0
    })

def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    }

    if keyboard is not None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    session.method("messages.send", post)


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        user_data = bot_api.users.get(user_ids = user_id)
        user_name = user_data[0]['first_name']
        keyboard = VkKeyboard()
        keyboard.add_button("Факты о Форте", VkKeyboardColor.POSITIVE)
        #keyboard.add_openlink_button('Купить билеты',
                                     #'https://rnd.kassir.ru/frame/selection/3058?key=e039ce40-6380-cce1-e21a-4c920955737d&WIDGET_592250029=2fl1des5q5ljgtl06umcr9876n')
        keyboard.add_button("Клубный мерч", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Расписание игр', VkKeyboardColor.POSITIVE)
        keyboard.add_button('Время до матча', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Полезные ссылки',VkKeyboardColor.POSITIVE)
        #keyboard.add_openlink_button('Расположение Форте Арены','https://yandex.ru/maps/971/taganrog/?ll=38.888405%2C47.204483&mode=poi&poi%5Bpoint%5D=38.888707%2C47.204746&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D94197634997&z=18.89')



        if text == 'начать' or text == 'start':
            send_message(user_id, f'Здравствуйте, {user_name}. Вас приветсвует бот футбольной команды Форте. Выберите один из пунктов главного меню.', keyboard)
        if text=='назад':
            send_message(user_id,' Вы вернулись в главное меню',keyboard)
        if text == 'клубный мерч':
            keyboard2 = VkKeyboard()
            i=0
            for key, value in parcer__shop().items():
                if i % 2 == 0 and i != 0:
                    keyboard2.add_line()
                keyboard2.add_openlink_button(key, value)
                i+=1
            keyboard2.add_line()
            keyboard2.add_button('Назад', VkKeyboardColor.NEGATIVE)
            send_message(user_id, 'В разделе "клубный мерч" вы можете приобрести сувениры и товары с символикой футбольного клуба.', keyboard2)




        if text == 'расписание игр':
            keyboard_raspis = VkKeyboard()
            keyboard_raspis.add_button("Расписание ФНЛ-2", VkKeyboardColor.PRIMARY)
            keyboard_raspis.add_button('Расписание кубка России', VkKeyboardColor.PRIMARY)
            keyboard_raspis.add_line()
            keyboard_raspis.add_button('Таблица первенства ФНЛ 2', VkKeyboardColor.PRIMARY)
            keyboard_raspis.add_button('назад',VkKeyboardColor.NEGATIVE)
            send_message(user_id,
                         'В разделе "расписание" вы можете узнать расписание игры ФК Форте.',
                         keyboard_raspis)
        if text=='расписание фнл-2':
            send_message(user_id,message='введите количество туров')
        elif text.isdigit():
            num_tours = int(text)
            send_message(user_id,turs(num_tours))
        if text=='расписание кубка россии':
            send_message(user_id,'К сожалению, ФК Форте закончил участие в Кубке России 2023-2024')



        if text == 'факты о форте':
            send_message(user_id, facts())
        if text == 'время до матча':
            keyboard_data = VkKeyboard()
            keyboard_data.add_button("Время до матча в ФНЛ-2", VkKeyboardColor.PRIMARY)
            keyboard_data.add_button('Время до матча в Кубке России', VkKeyboardColor.PRIMARY)
            keyboard_data.add_line()
            keyboard_data.add_button('назад', VkKeyboardColor.NEGATIVE)
            send_message(user_id,
                         'Здесь вы можете узнать время до ближайшего матча Форте',
                         keyboard_data)
        if text=='время до матча в фнл-2':
            send_message(user_id,date()[0])
        if text=='время до матча в кубке россии':
            send_message(user_id,'К сожалению, ФК Форте закончил участие в Кубке России 2023-2024')
        if text=='полезные ссылки':
            keyboard_links = VkKeyboard()
            keyboard_links.add_openlink_button('Купить билеты',
'https://rnd.kassir.ru/frame/selection/3058?key=e039ce40-6380-cce1-e21a-4c920955737d&WIDGET_592250029=2fl1des5q5ljgtl06umcr9876n')
            keyboard_links.add_openlink_button('Расположение Форте Арены','https://yandex.ru/maps/971/taganrog/?ll=38.888405%2C47.204483&mode=poi&poi%5Bpoint%5D=38.888707%2C47.204746&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D94197634997&z=18.89')
            keyboard_links.add_line()
            keyboard_links.add_button('назад',VkKeyboardColor.NEGATIVE)
            send_message(user_id,'Здесь вы можете найти полезную информацию',keyboard_links)
        if text=='таблица первенства фнл 2':
            send_message(user_id,table())


















