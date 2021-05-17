# 2. Написать функцию currency_rates(), принимающую в качестве аргумента код валюты (например, USD, EUR, GBP, ...)
# и возвращающую курс этой валюты по отношению к рублю. Использовать библиотеку requests.
# В качестве API можно использовать http://www.cbr.ru/scripts/XML_daily.asp.
# Рекомендация: выполнить предварительно запрос к API в обычном браузере, посмотреть содержимое ответа.
# Можно ли, используя только методы класса str, решить поставленную задачу?
# Функция должна возвращать результат числового типа, например float.
# Подумайте: есть ли смысл для работы с денежными величинами использовать вместо float тип Decimal?
# Сильно ли усложняется код функции при этом?
# Если в качестве аргумента передали код валюты, которого нет в ответе, вернуть None.
# Можно ли сделать работу функции не зависящей от того, в каком регистре был передан аргумент?
# В качестве примера выведите курсы доллара и евро.

import requests


def currency_rates(currency):
    """Возвращает курс обмена валют за сегодняшнюю дату"""

    # Здесь проверяем: если придет с консоли, то продет список. Значит возьмем нужное нам значение из списка
    if type(currency) == list:
        currency = currency[1]

    # Получаем хтмл страницу
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    encodings = requests.utils.get_encoding_from_headers(response.headers)
    content = response.content.decode(encoding=encodings)

    # Здесь начинается долгий процесс вычленения информации (читать в самом низу)
    tags = content.replace('/NumCode>', '')
    tags = tags.replace('/CharCode>', '')
    tags = tags.replace('/Name>', '')
    tags = tags.replace('/Value>', '')
    tags = tags.replace('/Valute>', '')
    tags = tags.replace('/Nominal>', '')
    tags = tags.split('<')
    del tags[0]
    del tags[0]

    # Забираем отсюда дату
    date = tags[0]
    date = date[14:24]

    # Продолжаем вычленять информацию
    del tags[0]
    tags.pop()
    for i in tags:
        if 'Valute' in i or len(i) == 0:
            tags.remove(i)
    for i in tags:
        if 'NumCode' in i or 'Nominal' in i:
            tags.remove(i)
    length = len(tags)
    for i in range(0, length):
        tags[i] = tags[i].split('>')
    for i in tags:
        i = i.pop(0)

    # Убираем '' из списка
    tags = [value for value in tags if value]

    # Убираем вложеный списки, да так плохо
    tags = sum(tags, [])

    # Создаем словарь из валют и их наименований
    length = len(tags)
    currency_rate = {}
    for i in range(0, length, 3):
        currency_value_and_full_name = tags[i + 1] + ': ' + tags[i + 2]
        currency_rate[tags[i]] = currency_value_and_full_name

    # Если пользователь ввел в нижнем регистре
    currency = currency.upper()

    # Достаем валюту из словаря
    currency = currency_rate.get(currency, 'Такой валюты в списке нет')
    print(currency)
    print(date)


# Для работы с консоли
if __name__ == '__main__':
    import sys

    exit(currency_rates(sys.argv))

# Все что происходит в функции - ужасно. Надеюсь на уроке я смогу понять как люди распарсили эту длинную строку.
# В чате мне объяснили мою проблему. Я делил по символу а нужно было все закатать в переменные и делить по целому тегу.
# Извините, что пришлось разбираться в этом мусоре. Но ведь работает - значит работает да?:)
# Честно, вместе с душой вложил еще и волю к жизни
