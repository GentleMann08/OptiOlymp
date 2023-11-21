from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import database

onoff = ['❌', '✅']

icons = {'Астрономия': ['🔭', 14], 'Математика': ['📏', 21], 'Русский язык': ['✍️', 22], 'Обществознание': ['👥', 23],
         'Литература': ['📚', 24], 'Испанский язык': ['🇪🇸', 25], 'География': ['🌍', 26], 'Технология': ['🛠️', 8],
         'История': ['📜', 27], 'Искусство (МХК)': ['🏛️', 28], 'Экономика': ['💹', 29], 'Право': ['⚖️', 30],
         'Биология': ['🍃', 31], 'Английский язык': ['🇬🇧', 32], 'Итальянский язык': ['🇮🇹', 33],
         'Китайский язык': ['🇨🇳', 34], 'Французский язык': ['🇫🇷', 35], 'Немецкий язык': ['🇩🇪', 36],
         'Экология': ['🌳', 7], 'Химия': ['🧪', 37], 'Информатика': ['💻', 47], 'Физическая культура': ['🏀', 48],
         'Физика': ['⚛️', 49],

         'Проектная программа': ['💘', 57],

         'Акварельная живопись': ['🖌️', 53],
         'Анималистическая скульптура': ['🍯', 53], 'Прикладное искусство': ['🧑‍🎨', 53],
         'Шахматы': ['♟️', 9]}

subjects = list(icons.keys())

iss_keys = {'Основы многослойной акварельной живописи': 'Акварельная живопись',
            'Основы декоративно-прикладного искусства': 'Прикладное искусство',
            'Основы анималистической скульптуры': 'Анималистическая скульптура'}

place_icons = {"АНОО «Физтех-лицей» им. П.Л. Капицы": ["💙", "Физтех-лицей"],
               "в дистанционном формате «Вебинар»": ["🤍", "Онлайн"],
               "АНОО «Областная гимназия им. Е. М. Примакова»": ["❤️", "Гимназия Примакова"],
               "ФГБОУ ВО «Академия акварели и изящных искусств Сергея Андрияки»": ["💚", "Академия Андрияки"],
               "ООО «СК Сатурн»": ["💜", "СК Сатурн"]}

title = {
    'Первая': "I",
    'Вторая': "II",
    'Третья': "III",
    'Четвертая': "IV",
    'Интенсивная профильная образовательная ': '',
    'интенсивная профильная образовательная ': '',
    'образовательная ': ''

}


def set_title(data: str):
    for i in title.keys():
        data = data.replace(i, title[i])
    data = data.split('(')[0].replace('программа', 'смена')
    if data[0] != 'I':
        data = data[0].lower() + data[1:]
    return data


mouth = {' января ': '.01.',
         ' февраля ': '.02.',
         ' марта ': '.03.',
         ' апреля ': '.04.',
         ' мая ': '.05.',
         ' июня ': '.06.',
         ' июля ': '.07.',
         ' августа ': '.08.',
         ' сентября ': '.09.',
         ' октября ': '.10.',
         ' ноября ': '.11.',
         ' декабря ': '.12.'}

graph = {'0': ["Наука", "Искусство", "Спорт"],

         "Наука": ["Языки", "Технические науки", "Естественные науки", "Гуманитарные науки", "Прочее"],
         "Искусство": ['Акварельная живопись', 'Анималистическая скульптура', 'Прикладное искусство'],
         "Спорт": ["Шахматы"],

         "Языки": ['Русский язык', 'Испанский язык', 'Английский язык',
                   'Итальянский язык', 'Китайский язык', 'Французский язык', 'Немецкий язык'],
         "Технические науки": ['Информатика', 'Математика', 'Технология'],
         "Естественные науки": ['Астрономия', 'Биология', "Экология", "Физика", "Химия"],
         "Гуманитарные науки": ['Обществознание', 'География', 'История', 'Искусство (МХК)', 'Экономика', 'Право',
                                'Литература'],
         "Прочее": ["Проектная программа", 'Физическая культура']
         }
back_graph = {}
for key in graph:
    for sub in graph[key]:
        back_graph[sub] = key
keys = [i for i in graph]

channel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='Подписаться',
        url='https://t.me/vzlet_group')]])


def set_url(url):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text='Перейти',
            url=url)]])


def set_back(now):
    return [InlineKeyboardButton(
        text='🚪 Назад',
        callback_data=back_graph[now])]


def olymp_button(user_id):
    temp = database.get(user_id, 'olymp')
    if not temp:
        temp = 0
    return InlineKeyboardButton(
        text=f'{onoff[temp]} Уведомления об олимпиадах',
        callback_data='olymp')


def set_middle_but(now, user_id):
    if now == '0':
        but = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=i,
                callback_data=i)] for i in graph[now]])
        but.inline_keyboard.append([olymp_button(user_id)])
        return but
    if graph[now][0] in subjects:
        notifs = database.get_notif(user_id)
        but = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=f'{i} - {onoff[notifs[subjects.index(i)]]}',
                callback_data=i)] for i in graph[now]])
        but.inline_keyboard.append(set_back(now))
        return but
    but = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=i,
            callback_data=i)] for i in graph[now]])
    but.inline_keyboard.append(set_back(now))
    return but


def set_notif(user_id, subject):
    notifs = database.set_notif(user_id, subjects.index(subject))
    now = ''
    for i in graph:
        for j in graph[i]:
            if subject in j:
                now = i
                break

    but = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=f'{i} - {onoff[notifs[subjects.index(i)]]}',
            callback_data=i)] for i in graph[now]])
    but.inline_keyboard.append(set_back(now))
    return but


settings = KeyboardButton(text='🔔 Настройка уведомлений')

main_menu = ReplyKeyboardMarkup(keyboard=[[settings]],
                                resize_keyboard=True)

# olymp_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[[reboot]])

if __name__ == "__main__":
    pass
