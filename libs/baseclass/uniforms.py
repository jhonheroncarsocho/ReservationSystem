import sqlite3
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.clock import Clock


Builder.load_file('./libs/kv/uniforms.kv')


class UniformCard(MDCard):
    index = NumericProperty()
    name = StringProperty('')
    image = StringProperty('')
    stocks = NumericProperty(0)
    price = StringProperty('')
    icon = StringProperty()
    title = StringProperty()
    count = NumericProperty(0)


class Uniforms(Screen):
    def __init__(self, **kwargs):
        super(Uniforms, self).__init__(**kwargs)

    def on_enter(self, *args):
        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)
                store_widgets = UniformCard(index=info[0], name=info[1], price=info[2], stocks=info[3])
                self.ids.content.add_widget(store_widgets)

        asynckivy.start(on_enter())

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS shop(id integer unique primary key autoincrement, items, price,"
                       " stocks)")
        cursor.execute('SELECT * from shop WHERE category = "Uniform"')
        rows = cursor.fetchall()

        for row in rows:
            data_items.append(row)

        conn.close()

        return data_items  # data_items

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
