from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivy.clock import Clock

import sqlite3

Builder.load_file('./libs/kv/store.kv')

class Card(MDCard):
    index = NumericProperty()
    icon = StringProperty()
    title = StringProperty()


class Store(Screen):
    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)

    def on_enter(self, *args):
        data_items = self.store_direct()

    #     async def on_enter():
    #         for info in data_items:
    #             await asynckivy.sleep(0)
    #             store_widgets = Card()
    #             self.ids.content.add_widget(store_widgets)
    #
    #     asynckivy.start(on_enter())
    #
    # def refresh_callback(self, *args):
    #     '''A method that updates the state of your application
    #     while the spinner remains on the screen.'''
    #
    #     def refresh_callback(interval):
    #         self.ids.content.clear_widgets()
    #
    #         if self.x == 0:
    #             self.x, self.y = 0, 0
    #         else:
    #             self.x, self.y = 0, 0
    #         self.on_enter()
    #         self.ids.refresh_layout.refresh_done()
    #
    #     Clock.schedule_once(refresh_callback, 1)

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS shop(id integer unique primary key autoincrement, usr_id)")

        # for row in rows:
        #     data_items.append(row)

        conn.close()

        return data_items  # data_items

    def on_press(self, instance):
        pass

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
