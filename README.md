## 1.Что это такое ?

Этот код позволяет найти самый большой, самый маленький и ближайший бар из списка(который должен быть представлен в виде JSON-структуры передаваемой как аргумент) 

## 2.Системные требования
Для работы с программой понадобится Python3.5 (который скорее всего у вас уже установлен, если Вы используете Linux)  
Также может понадобиться установить модуль `geopy`, сделать это можно выполнив `pip3.5 install -r requirements.txt`
```
# pip3.5 install -r requirements.txt
```

## 3.Где можно скачать  
Можно форкнуть здесь - [ближайшие бары](https://github.com/aligang/3_bars)  
и затем скачать 
```
git clone https://github.com/<юзернейм-аккаунта-на-гите>/3_bars
```

## 4.Как этим пользоваться...  
*a.Данный код может быть исползован как самостоятельная программа,*  
*при этом программа попросит Вас  сначала указать файл с JSON, а затем координаты GPS, относительно которых будет найден ближайший бар*

```bash
$ python3.5 bars.py <path to file>
Самый большой бар в округе: Спорт бар «Красная машина»
Который расположен по адресу: Автозаводская улица, дом 23, строение 1
Самый маленький бар в округе: БАР. СОКИ
Который расположен по адресу: Дубравная улица, дом 34/29
Введите  GPS  координаты, подыщем ближайший бар: 70.70 70.70
Ближайший бар : Таверна
Который расположен по адресу: проспект Защитников Москвы, дом 8
Находится на расстоянии 3669 километров

```
*b. Функции могут быть импортированы в Ваш код (пример в разделе 5)*


## 5.Какие функции могут быть переиспользованы в вашем коде
Функция `load_data` читает структуру raw-JSON из файла и преобразует её в python-обект.  
Функция `get_biggest_bar` находит самый большой бар, упоминающийся в JSON,  
возвращает dict в котором содержится информация об этом баре  
Функция `get_smallest_bar` находит самый маленький бар, упоминающийся в JSON,  
возвращает dict в котором содержится информация об этом баре  
Функция `get_сloset_bar` находит ближайший бар, упоминающийся в JSON, отностительно координат, подаваемых как аргументы функции,  
возвращает dict в котором содержится информация об этом баре, а также float, которая отражает расстояние в метрах от заданных GPS координат до этого бара  
Функция `request_user_defined_coordinates` запрашивает GPS координаты через поток ввода/вывода  
Функция `get_pretty_output` выводит информацию о барах на поток ввода/вывода


Импортировать и использовать функцию коди можно  следующим образом:  
```python
from bars import load_data
from bars import get_closest_bar
from bars import get_biggest_bar
from bars import get_smallest_bar

object_representing_json = load_data(filepath)
closest_bar = get_closet_bar(object_representing_json, user_defined_longitude, user_defined_latitude)
biggest_bar = get_biggest_bar(object_representing_json, user_defined_longitude, user_defined_latitude)
```

## 6. Цели
Код создан в учебных целях. В рамках учебного курса по веб-разработке ― [DEVMAN.org](https://devman.org)