

import datetime as dt   # библиотека работы с датами, временем и тд
import requests     # библиотека запросов HTTP
# База друзей Анфисы
DATABASE = {
    'Сергей': 'Омск',
    'Соня': 'Москва',
    'Алексей': 'Калининград',
    'Миша': 'Москва',
    'Дима': 'Челябинск',
    'Алина': 'Красноярск',
    'Егор': 'Пермь',
    'Коля': 'Красноярск',
    'Артём': 'Владивосток',
    'Петя': 'Михайловка'
}
# часовые пояса
UTC_OFFSET = {
    'Москва': 3,
    'Санкт-Петербург': 3,
    'Новосибирск': 7,
    'Екатеринбург': 5,
    'Нижний Новгород': 3,
    'Казань': 3,
    'Челябинск': 5,
    'Омск': 6,
    'Самара': 4,
    'Ростов-на-Дону': 3,
    'Уфа': 5,
    'Красноярск': 7,
    'Воронеж': 3,
    'Пермь': 5,
    'Волгоград': 3,
    'Краснодар': 3,
    'Калининград': 2,
    'Владивосток': 10
}

# функция грамотно корректирует текст для вывода
def format_count_friends(count_friends):
    if count_friends == 1:
        return '1 друг'
    elif 2 <= count_friends <= 4:
        return f'{count_friends} друга'
    else:
        return f'{count_friends} друзей'

# функция выводит время полученного в аргументах города
def what_time(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime("%H:%M")
    return f_time

# функция возвращает значение погоды в нужном Городе
def what_weather(city):
    url = f'http://wttr.in/{city}'  # адрес сервера погоды
    weather_parameters = {          # задаем в каком формате выводить на экран погоду
        'format': 2,
        'M': ''
    }
    try:    # перехват исключения, чтобы не было ошибок при работе
        response = requests.get(url, params=weather_parameters) # делаем запрос на сервер с параметрами
    except requests.ConnectionError:    # исключение ошибки
        return '<сетевая ошибка>'
    if response.status_code == 200:     # код 200 означает ОК, запрос на сервер прошел успешно
        return response.text            # вывод Погоды
    else:
        return '<ошибка на сервере погоды>'

# Анфиса отвечает на вопросы
def process_anfisa(query):
    if query == 'сколько у меня друзей?':
        count = len(DATABASE)                           # содержит количество друзей
        return f'У тебя {format_count_friends(count)}.' # переход в функцию для грамотного вывода текста
    elif query == 'кто все мои друзья?':
        friends_string = ', '.join(DATABASE)  # получает значиния из словаря и разделяет их запятой преобразовав в строку
        return f'Твои друзья: {friends_string}'
    elif query == 'где все мои друзья?':
        unique_cities = set(DATABASE.values()) # значения из словаря преобразует в множество, чтобы не повторялись
        cities_string = ', '.join(unique_cities)  # преобразует множество в строку и разделяет запятой
        return f'Твои друзья в городах: {cities_string}'
    else:
        return '<неизвестный запрос>'

# функция отвечает на вопросы друзьям
def process_friend(name, query):
    if name in DATABASE:        # если имя друга есть в базе
        city = DATABASE[name]   # присваиваем значение по ключ из словаря
        if query == 'ты где?':
            return f'{name} в городе {city}'
        elif query == 'который час?':
            if city not in UTC_OFFSET:      # ищет город в базе часовых поясов
                return f'<не могу определить время в городе {city}>'
            time = what_time(city)      # вызывает функцию которая возвратит время нужном городе
            return f'Там сейчас {time}'
        elif query == 'как погода?':
            weather = what_weather(city)    # вызывает функцию, которая возвращает погоду в нужном Городе
            return weather
        else:
            return '<неизвестный запрос>'
    else:
        return f'У тебя нет друга по имени {name}'

# Функция получает вопрос и разделяет его и смотрит на первый элемент, кому был задан вопрос
# Анфисе или Другу
def process_query(query):
    elements = query.split(', ')
    if elements[0] == 'Анфиса':
        return process_anfisa(elements[1])      # если вопрос Анфисе вызываем функцию process_anfisa
    else:
        return process_friend(elements[0], elements[1])     # если другу вызываем функцию process_friend

# функция возвращает список с вопросами Анфисе
def runner():
    queries = [
        'Анфиса, сколько у меня друзей?',
        'Анфиса, кто все мои друзья?',
        'Анфиса, где все мои друзья?',
        'Анфиса, кто виноват?',
        'Коля, ты где?',
        'Соня, что делать?',
        'Антон, ты где?',
        'Алексей, который час?',
        'Артём, который час?',
        'Антон, который час?',
        'Петя, который час?',
        'Коля, как погода?',
        'Соня, как погода?',
        'Антон, как погода?'
    ]
# циклом задаем вопросы и получаем ответы
    for query in queries:
        print(query, '-', process_query(query))

runner()