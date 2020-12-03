# API для отслеживания числа объявлений на avito.ru
## Технологии:
- Python 3.7
- FastAPI
- Selenium для парсинга. Selenium использует chromdriver, поэтому лучше устновить его перед запуском, в случае если моя версия не работает
- SQLite для хранения данных сервиса
- Docker
- Pydantic  для создания моделей

## Методы:
 - `/add`- Метод регистрирует пару. Принимает два значения: phrase (*string*) и region (*string*), возвращает id добавленной пары. Если пара была в системе ранее то вернется существующее ранее id, если она новая, то значения будут добавлены в базу данных и вернется id новой пары. После добавления дла пары каждый час будут считаться топ 5 объявлений и число объявлений.
 
 - `/stat` - Метод возвращает пары (*временная_метка*: *счетчик_числа_объявлений*). Число объявлений вычисляется каждый час и добавляется в базу данных в таблицу *TimeStamps*. На вход методу подается id (*string*) пары, зарегистрированной в системе
 
 - `/get_top` - Метод возвращает список ссылок на топ-5 объявлений. Принимает id (*string*) пары, которая зарегистрированна в системе