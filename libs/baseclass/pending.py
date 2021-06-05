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

Builder.load_file('./libs/kv/pending.kv')

class PendingCard(MDCard):
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

    def delete_item(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()
        cursor.execute(f'DELETE from pending where id = {self.index} and usr_id = {uid[0]}')
        conn.commit()
        conn.close()
        self.parent.remove_widget(self)


class Pending(Screen):
    def __init__(self, **kwargs):
        super(Pending, self).__init__(**kwargs)

        self.get = MDApp.get_running_app()

    def on_enter(self, *args):
        self.get.product_category = 'Book'
        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)

                reserve_widgets = PendingCard(index=info[0], product_id=info[2], name=info[3], price=info[4],
                                              count=info[5], category=info[6])

                self.ids.content.add_widget(reserve_widgets)

        asynckivy.start(on_enter())

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute('CREATE TABLE IF NOT EXISTS pending(id integer unique primary key autoincrement, usr_id, '
                       'product_id, name, price, stocks, count, category)')
        cursor.execute(f'SELECT * FROM pending WHERE usr_id = {uid[0]}')

        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)

        return data_items  # data_items

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
