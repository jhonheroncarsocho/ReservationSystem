import sqlite3
from kivy.config import Config
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty
from libs.baseclass import nav_screen, store, uniforms, books, cart, login, pending, register, uniforms2


class MyApp(MDApp):
    product_category = StringProperty()
    log_usr = StringProperty()
    product_index = NumericProperty()
    selected = StringProperty('')
    selected2 = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Take a Number'

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run

    def on_start(self):
        if self.get_account() is not None and self.get_account() != []:
            print(self.get_account())
            self.root.current = 'nav_screen'
        else:
            self.root.current = 'login'

    def get_account(self):
        try:
            conn = sqlite3.connect('./assets/data/app_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE status = "active"')
            data = cursor.fetchone()
        except (AttributeError, sqlite3.OperationalError):
            data = None
        return data

    def colors(self, color_code):
        if color_code == 0:
            color_rgba = '#f3cdc0'
        elif color_code == 1:
            color_rgba = '#00539CFF'
        elif color_code == 2:
            color_rgba = '#4a2c27'

        return color_rgba

    def show_screen(self, name):
        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True


if __name__ == "__main__":
    Config.set("graphics", "width", "1180")

    Config.set("graphics", "height", "800")
    Config.write()
    MyApp().run()
