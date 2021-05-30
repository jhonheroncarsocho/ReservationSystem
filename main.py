import kivy
import sqlite3
from kivy.config import Config
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from libs.baseclass import nav_screen

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run

    def show_screen(self, name):
        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True


if __name__ == "__main__":
    Config.set("graphics", "width", "800")
    Config.set("graphics", "height", "500")
    Config.write()
    MyApp().run()
