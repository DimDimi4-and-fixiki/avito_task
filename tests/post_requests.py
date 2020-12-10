import pytest
import requests
import json

#  regions for requests:

cities = ["Москва", "Владивосток", "Саратов", "fdsfdsd",
                       "Нижний Новгород", "Самара",
                       "Белгород", "Якутск", "Ржев",
                       "Хабаровск", "Новосибирск", "Казань",
                       "Северодвинск", "Иркутск", "Брянск",
                       "Мурманск", "Калининград", "Смоленск",
                       "Омск", "Анапа", "Сочи", "Курск",
                       "Челябинск", "Красноярск", "Воронеж",
                       "Тюмень", "Уфа", "Краснодар",
                       "Ярославль", "Чехов", "Барнаул",
                       "Махачкала", "Томск", "Кемерово",
                       "Чебоксары", "Магнитогорск", "Тверь",
                       "Севастополь", "Ставрополь", "Архангельск",
                       "Орел", "Подольск", "Петрозаводск",
                       "Тамбов", "Владикавказ", "Кострома"]

#  phrases for requests:

phrases = ["Елка", "Смартфон", "jfkdjfk", "оаоаооаао", "Кошка",
                      "Чайник", "Носки", "RJ45",
                      "Компьютер", "Кроссовки", "Ковер",
                      "Книга", "Библия", "Мяч",
                      "Мармелад", "Игрушка", "Аквариум",
                      "Машина", "Квартира", "Лампа",
                      "Одеяло", "Батончик", "Гладильная доска",
                      "Чашка", "Чехол", "Доширак",
                      "Куллер", "Аккумулятор", "Парфюм",
                      "Лента от мух", "Модем", "Холодильник",
                      "HQD", "Тетрадь", "Члиииисссс",
                      "Кукла", "Футболка", "Трусы",
                      "Зубная щетка", "Пылесос", "Диск",
                      "Пазл", "Диплом", "Руль",
                      "Женщина", "Краска", "Парик",
                      "Серьги", "Кольцо", "Сумка",
                      "Шуба", "Мясорубка", "Миксер",
                      "Блендер", "Блузка", "Куртка",
                      "Самокат", "Маска", "Перчатки"]

pairs = []  # pairs of (phrase, region)
url = "http://0.0.0.0:80/add"  # url for requests

for phrase in phrases:
    for city in cities:
        pairs.append([phrase, city])  # adding new pair


@pytest.mark.parametrize("pair", pairs[:600])
def test_post_requests(pair):
    """
    Tests if add request returns OK
    :param pair:  pair of (phrase, region)
    :return:
    """
    phrase_name = pair[0]  # phrase
    region = pair[1]  # region

    headers = {'Content-Type': 'application/json'}

    payload = {'phrase': phrase_name, 'region': region}  # data in a dictionary
    response = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    assert response.status_code == 200  # checks if response is OK










