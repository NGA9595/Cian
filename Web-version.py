import _pickle as cPickle
import pandas as pd
import numpy as np
import re
from sklearn import model_selection
from sklearn import preprocessing
import cherrypy as cherrypy
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
import requests
from bs4 import BeautifulSoup
class PredictGenerator(object):
    def One_Flat_Downloader(self, link_flat):


        data = { }  # Задали пустой словарь, в который мы будем сохранять данные

    # Подгружаем страничку с информацией по квартире
        response = requests.get(link_flat)
        html = response.content
        soup = BeautifulSoup(html,'html.parser')


        # Вытаскиваем цену на квартиру
        try:
            price = soup.findAll('span', attrs = {'itemprop':"price"})[0].text.strip()
            data['Цена'] = price
        except Exception:
            data['Цена'] = "NaN"

        #Вытаскиваем балкон/лоджия
        try:
            balkon = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Балкон/лоджия'] = balkon
        except Exception:
            data['Балкон/лоджия'] = "NaN"

        # Вытаскиваем вид из окон
        try:
            vid_na_okna =  soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Вид из окон'] = vid_na_okna
        except Exception:
            data['Вид из окон'] = 'NaN'

        # Вытаскиваем высоту потолков
        try:
            visota_potolkov = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Высота потолков'] = visota_potolkov
        except Exception:
            data['Высота потолков'] = 'NaN'

        # Вытаскиваем расстояние до метро то ли пешком то ли на машине...
        try:
            Do_metro = soup.findAll('span', attrs = {'class':"a10a3f92e9--underground_time--1fKft"})[0].text.strip()
            data['До метро'] = Do_metro
        except Exception:
            data['До метро'] = "NaN"

        # Вытаскиваем метро
        try:
            station = soup.findAll('ul', attrs = {'class':"a10a3f92e9--undergrounds--2pop3"})[0].a.text
            data['Метро'] = station
        except Exception:
            data['Метро'] = "NaN"

        #Вытаскиваем отделку
        try:
            otdelka = soup.findAll('data-name', attrs = {'class': 'a10a3f92e9--container--fVifv'})[0].text.strip()
            data['Отделка'] = otdelka
        except Exception:
            data['Отделка'] = 'NaN'

        #Вытаскиваем планировку
        try:
            planirovka = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Планировка'] = planirovka
        except Exception:
            data['Планировка'] = "NaN"

        # Вытаскиваем площадь комнаты
        try:
            ploshad = soup.findAll('div', attrs = {'class':"a10a3f92e9--info-value--18c8R"})[0].text.strip()
            data['Площадь комнат'] = ploshad
        except Exception:
            data['Площадь комнат'] = "NaN"

        #Вытаскиваем ремонт
        try:
            remont = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Ремонт'] = remont
        except Exception:
            data['Ремонт'] = "NaN"

        #Вытаскиваем санузел
        try:
            sanuzel = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Санузел'] = sanuzel
        except Exception:
            data['Санузел'] = "NaN"


        #Вытаскиваем адрес
        try:
            adress = soup.findAll('address', attrs = {'class':"a10a3f92e9--address--140Ec"})[0].text.strip()
            data['Адрес'] = adress
        except Exception:
            data['Адрес'] = "NaN"

        # Вытаскиваем тип жилья
        try:
            typeflat = soup.findAll('data-name', attrs = {'class':"a10a3f92e9--container--fVifv"})[0].text.strip()
            data['Тип жилья'] = typeflat
        except Exception:
            data['Тип жилья'] = "NaN"


        # Вытаскиваем количество комнат в квартире
        try:
            komnata = soup.findAll('h1', attrs = {'class':"a10a3f92e9--title--2Widg"})[0].text.strip()
            data['Комнаты'] = komnata
        except Exception:
            data['Комнаты'] = "NaN"

        # Вытаскиваем санузел в квартире
        sanuzel = soup.findAll('li', attrs = {'class':"a10a3f92e9--item--_ipjK"})
        for i in sanuzel:
            name = i.findAll('span', attrs = {'class': "a10a3f92e9--name--3bt8k"})[0].text.strip()
            value = i.findAll('span', attrs = {'class': "a10a3f92e9--value--3Ftu5"})[0].text.strip()
            data[name] = value



        df = data

        df = pd.DataFrame([df])

        d = {'Во двор' : 2, 'На улицу' : 1, 'На улицу и двор' : 3}
        df['Вид из окон'] = df['Вид из окон'].map(d)
        df['Вид из окон'] = df['Вид из окон'].fillna(2)
        metro =  {i: 1 for i in df['Метро'].value_counts().keys()}
        df['Метро'] = df['Метро'].map(metro)
        df['Метро'] = df['Метро'].fillna(0)
        balcon = {'1 лоджия' : 2, '1 балкон' : 1, '2 лоджии' : 4, '2 балкона' : 2, '1 балкон, 1 лоджия' : 3, '3 лоджии' : 6, '4 балкона' : 4, '3 балкона' : 3, '2 балкона, 1 лоджия' : 4, '2 балкона, 2 лоджии' : 6, '3 балкона, 3 лоджии' : 9, '2 балкона, 3 лоджии' : 8, '4 лоджии' : 8, '1 балкон, 2 лоджии': 5}
        df['Балкон/лоджия'] = df['Балкон/лоджия'].map(balcon)
        df['Балкон/лоджия'] = df['Балкон/лоджия'].fillna(0)
        df['Высота потолков'] = df['Высота потолков'].astype('str')
        def high(x):
            return x.split(' ')[0]
        df['Высота потолков'] = df['Высота потолков'].apply(high)
        def to_float(x):
            return x.replace(',', '.')
        df['Высота потолков'] = df['Высота потолков'].apply(to_float)
        df['Высота потолков'] = df['Высота потолков'].astype('float')
        df['Высота потолков'] = df['Высота потолков'].fillna(3)
        otdelka = {'Нет' : 0, 'Чистовая' : 1, 'Черновая' : 0}
        df['Отделка'] = df['Отделка'].map(otdelka)
        df['Отделка'] = df['Отделка'].fillna(0)
        type_flat = {'Вторичка' : 1, 'Вторичка Апартаменты' : 1.5, 'Новостройка' : 2, 'Новостройка Апартаменты' : 2.5}
        df['Тип жилья'] = df['Тип жилья'].map(type_flat)
        remont = {'Без ремонта' : 0, 'Косметический' : 1, 'Евроремонт' : 1.5, 'Дизайнерский' : 2}
        df['Ремонт'] = df['Ремонт'].map(remont)
        df['Ремонт'] = df['Ремонт'].fillna(0)
        planirovka = {'Изолированная' : 2, 'Смежно-изолированная' : 1.5, 'Смежная' : 1}
        df['Планировка'] = df['Планировка'].map(planirovka)
        df['Планировка'] = df['Планировка'].fillna(1)
        def sv(x):
            return x.replace('свободной' , 'квартира')
        df['Комнаты'] = df['Комнаты'].apply(sv)
        def apart(x):
            return x.split(' ')[1]
        df['Комнаты'] = df['Комнаты'].apply(apart)
        def delcom(x):
            return x.replace(',' , '')
        df['Комнаты'] = df['Комнаты'].apply(delcom)
        df['Площадь комнат'].astype('str')
        def split(x):
            return x.split('м')[0]
        df['Площадь комнат'] = df['Площадь комнат'].apply(split)
        df['Площадь комнат'] = df['Площадь комнат'].apply(to_float)
        df['Площадь комнат'] = df['Площадь комнат'].astype('float')
        sanuzel = {'1 совмещенный' : 1, '1 совмещенный, 1 раздельный' : 2.5, '1 совмещенный, 2 раздельных' : 4,
                   '1 раздельный' : 1.5,  '1 совмещенный, 4 раздельных' : 7,  '2 совмещенных' : 2, '2 раздельных' : 3,
                   '2 совмещенных, 1 раздельный': 3.5, '2 совмещенных, 2 раздельных' : 5, '2 совмещенных, 3 раздельных' : 6.5,
                   '3 совмещенных' : 3, '3 совмещенных, 1 раздельный' : 4.5, '3 раздельных' : 4.5,
                   '4 совмещенных' : 4, '4 совмещенных, 1 раздельный' : 5.5, '4 совмещенных, 3 раздельных' : 8.5,
                   '4 совмещенных, 4 раздельных' : 10, '4 совмещенных, 2 раздельных' : 7, '4 раздельных' : 6}
        df['Санузел'] = df['Санузел'].map(sanuzel)
        df['Санузел'] = df['Санузел'].fillna(1)
        def adress(x):
            return x.split(',')[1]
        df['Адрес'] = df['Адрес'].apply(adress)
        df['До метро'] = df['До метро'].astype('str')
        def to_metro(x):
            return x.replace('⋅', '')
        df['До метро'] = df['До метро'].apply(to_metro)
        def how_to_metro(x):
            return x.split(' ')[-1]
        df['Как добраться'] = df['До метро'].apply(how_to_metro)
        def to_metro1(x):
            return x.split('мин')[0]
        df['До метро'] = df['До метро'].apply(to_metro1)
        def otkroetsa(x):
            return x.replace('откроется в 2021', '0') .replace('откроется в 2020', '0') .replace('<1', '1') .replace('откроется в 2022', '0')
        df['До метро'] = df['До метро'].apply(otkroetsa)
        df['До метро'] = df['До метро'].astype('float')
        df['До метро'] = df['До метро'].fillna(0)
        def kak_dobratsya(x):
            return x.replace('пешком', '1') .replace('2020', '0') .replace('транспорте', '2') .replace('2021', '0') .replace('2022', '0')
        df['Как добраться'] = df['Как добраться'].apply(kak_dobratsya)
        df['Как добраться'] = df['Как добраться'].fillna(0)
        df['Как добраться'] = df['Как добраться'].astype('int')
        def price(x):
            return x.replace('₽', '')
        df['Цена'] = df['Цена'].apply(price)
        df['Цена'] = df['Цена'].apply(lambda x: ''.join(re.findall(r'[0-9]+', x)))
        df['Цена'] = df['Цена'].astype('int64')
        df['Адрес_ ВАО'] = 0
        df['Адрес_ ЗАО'] = 0
        df['Адрес_ НАО (Новомосковский)'] = 0
        df['Адрес_ САО'] = 0
        df['Адрес_ СВАО'] = 0
        df['Адрес_ СЗАО'] = 0
        df['Адрес_ ТАО (Троицкий)'] = 0
        df['Адрес_ ЦАО'] = 0
        df['Адрес_ ЮАО'] = 0
        df['Адрес_ ЮВАО'] = 0
        df['Адрес_ ЮЗАО'] = 0
        df['Комнаты_апартаменты'] = 0
        df['Комнаты_квартира'] = 0
        df['Адрес_' + df['Адрес']] = 1
        df = df.drop(['Адрес'], axis = 1)
        df['Комнаты_' + df['Комнаты']] = 1
        df = df.drop(['Комнаты'], axis = 1)
        df = df.drop(['Цена'], axis = 1)

        return df


    @cherrypy.expose
    def index(self):
        return """<html>
            <head></head>
            <body>
                <form method="get" action="generate">
                    <input type="text" value="" name="link_flat" />
                    <button type="submit">Predict!</button>
                </form>
            </body>
        </html>"""
    @cherrypy.expose
    def generate(self, link_flat):
        # bdt = BaggingRegressor(RandomForestRegressor()).fit(x_train, y_train)
        with open('CIAN_data.pkl', 'rb') as fid:
            dt_load = cPickle.load(fid)
            df = self.One_Flat_Downloader(link_flat)

            predict = 'predict price {}'.format(dt_load.predict(df)[0])
            cherrypy.session['predict'] = predict

        return predict
    @cherrypy.expose
    def display(self):
        return cherrypy.session['predict']

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    cherrypy.config.update({'server.socket_port': 8098})
    cherrypy.quickstart(PredictGenerator(), '/', conf)
    
