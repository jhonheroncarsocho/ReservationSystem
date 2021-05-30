from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivy.clock import Clock

Builder.load_file('./libs/kv/home.kv')

class Card(MDCard):
    index = NumericProperty()
    icon = StringProperty()
    title = StringProperty()


class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)