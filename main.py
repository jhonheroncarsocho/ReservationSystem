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
from libs.baseclass import nav_screen, home


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run

    def colors(self, color_code):
        if color_code == 0:
            color_rgba = '#f3cdc0'
        elif color_code == 1:
            color_rgba = '#ffddce'
        elif color_code == 2:
            color_rgba = '#4a2c27'

        return color_rgba

    def show_screen(self, name):
        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True


if __name__ == "__main__":
    Config.set("graphics", "width", "1000")
    Config.set("graphics", "height", "800")
    Config.write()
    MyApp().run()
