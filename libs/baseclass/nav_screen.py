import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

Builder.load_file('./libs/kv/nav_screen.kv')


class NavLayout(Screen):
    def __init__(self, **kwargs):
        super(NavLayout, self).__init__(**kwargs)

    def logout(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET status = "inactive" WHERE status = "active"')
        conn.commit()
        conn.close()
