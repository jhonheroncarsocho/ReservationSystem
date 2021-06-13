from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

Builder.load_file('./libs/kv/store.kv')

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class Store(Screen):
    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)

    def on_enter(self):
        pass
