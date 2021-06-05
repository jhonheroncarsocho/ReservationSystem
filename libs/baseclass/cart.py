import sqlite3
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.tab import MDTabsBase
from kivy.clock import Clock

Builder.load_file('./libs/kv/cart.kv')

class CartCard(MDCard):
    index = NumericProperty()
    product_id = NumericProperty()
    name = StringProperty('')
    image = StringProperty('')
    stocks = NumericProperty(0)
    price = StringProperty('')
    icon = StringProperty()
    title = StringProperty()
    count = NumericProperty(0)
    category = StringProperty('')

    def update(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE cart SET count = {self.count} WHERE id = {self.index}')
        conn.commit()
        conn.close()

class Cart(Screen):
    def __init__(self, **kwargs):
        super(Cart, self).__init__(**kwargs)

        self.get = MDApp.get_running_app()

    def on_enter(self, *args):
        self.get.product_category = 'Book'
        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)
                reserve_widgets = CartCard(index=info[0], product_id=info[1], name=info[2], price=info[3],
                                           stocks=info[4], count=info[5], category=info[6])

                self.ids.content.add_widget(reserve_widgets)

        asynckivy.start(on_enter())

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS cart(id integer unique primary key autoincrement, product_id, name, '
                       'price, stocks, count, category)')
        cursor.execute('SELECT * FROM cart')

        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)

        print(data_items)
        return data_items  # data_items

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
