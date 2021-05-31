from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd_extensions.akivymd import *

Builder.load_file('./libs/kv/nav_screen.kv')


class NavLayout(Screen):
    def __init__(self, **kwargs):
        super(NavLayout, self).__init__(**kwargs)
