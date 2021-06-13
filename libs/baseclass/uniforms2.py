import sqlite3
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors


Builder.load_file('./libs/kv/uniforms2.kv')


class UniformCard2(MDCard):
    index = NumericProperty()
    name = StringProperty('')
    image = StringProperty('')
    stocks = NumericProperty(0)
    price = StringProperty('')
    icon = StringProperty()
    title = StringProperty()
    count = NumericProperty(0)
    category = StringProperty()

    def to_cart(self):
        get = MDApp.get_running_app()
        if get.selected2 != '':
            conn = sqlite3.connect('./assets/data/app_data.db')
            cursor = conn.cursor()

            cursor.execute(f'SELECT id FROM accounts WHERE status = "active"')
            uid = cursor.fetchone()
            cursor.execute('CREATE TABLE IF NOT EXISTS cart(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, usr_id, '
                           'product_id, name, price, stocks, count, size)')
            cursor.execute(f'SELECT * FROM cart where product_id = {self.index} and usr_id = {uid[0]} and '
                           f'size = "{get.selected}"')
            get_product = cursor.fetchone()
            if get.selected2 != '':
                if get_product is None:
                    insert = 'INSERT INTO cart (usr_id, product_id, name, price, stocks, count, size, category) ' \
                             'VALUES (?,?,?,?,?,?,?,?)'
                    cursor.execute(insert, (uid[0], self.index, self.name, self.price,  self.stocks, 1, get.selected, self.category))
                else:
                    if get_product[7] == get.selected:
                        cursor.execute(f'SELECT count FROM cart WHERE product_id = {self.index} and size = "{get.selected}"')
                        get_count = cursor.fetchone()
                        if get_count[0] != self.stocks:

                            cursor.execute(f'UPDATE cart SET count = {get_count[0] + 1} WHERE product_id = {self.index} '
                                           f'and usr_id = {uid[0]} and size = "{get.selected}"')
                    else:
                        insert = 'INSERT INTO cart (usr_id, product_id, name, price, stocks, count, size, category) ' \
                                 'VALUES (?,?,?,?,?,?,?,?)'
                        cursor.execute(insert, (uid[0], self.index, self.name, self.price, self.stocks, 1, get.selected, self.category))

                conn.commit()
                conn.close()
            get.selected2 = ''
        else:
            print('Select Size')


class PlanItem2(ThemableBehavior, MagicBehavior, MDBoxLayout):
    text_item = StringProperty()
    border = StringProperty()
    color_select = ListProperty()
    selected = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_select = self.theme_cls.disabled_hint_text_color
        self.primary = get_color_from_hex(colors["BlueGray"]["500"])
        self.get = MDApp.get_running_app()

    def press_on_plan(self, instance_plan):
        for widget in self.parent.parent.children[0].children:
            if widget.color_select == self.primary:
                widget.color_select = self.color_select
                self.grow()
                break
        instance_plan.color_select = self.primary
        self.get.selected2 = instance_plan.text_item


class Uniforms2(Screen):
    def __init__(self, **kwargs):
        super(Uniforms2, self).__init__(**kwargs)
        self.get = MDApp.get_running_app()

    def on_enter(self, *args):

        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)

                store_widgets = UniformCard2(index=info[0], name=info[1], price=info[2], stocks=info[3], category=info[4])

                self.ids.content.add_widget(store_widgets)

        asynckivy.start(on_enter())

    def store_direct(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
                       id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, 
                       items TEXT, 
                       price INTEGER,
                       stocks INTEGER)
                       """)
        cursor.execute('SELECT * FROM shop WHERE category = "Bottom"')
        rows = cursor.fetchall()

        conn.close()

        return rows  # data_items
