import sqlite3
import datetime
import random
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty, NumericProperty
from kivy.factory import Factory
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivy.utils import get_color_from_hex
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton


Builder.load_file('./libs/kv/cart.kv')

class CartCard(MDCard):
    index = NumericProperty()
    product_id = NumericProperty()
    name = StringProperty('')
    image = StringProperty('')
    stocks = NumericProperty(0)
    price = StringProperty('')
    icon = StringProperty()
    title = StringProperty()
    count = NumericProperty(0)
    size_item = StringProperty()
    category = StringProperty('')

    def update(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()
        cursor.execute(f'UPDATE cart SET count = {self.count} WHERE id = {self.index} and usr_id = {uid[0]}')
        conn.commit()
        conn.close()

    def delete_item(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()
        cursor.execute(f'DELETE from cart where id = {self.index} and usr_id = {uid[0]}')
        conn.commit()
        conn.close()
        self.parent.remove_widget(self)
        Snackbar(text='Item is deleted').open()

class IconListItem(OneLineIconListItem):
    icon = StringProperty('weather-sunny')


class ConfirmDialog(BoxLayout):
    selected_date = StringProperty('')

    # fOR DROPDOWN
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        shift = ['MORNING', 'AFTERNOON']
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "height": dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in shift]

        self.menu = MDDropdownMenu(
            caller=self.ids.field,
            items=menu_items,
            position="auto",
            width_mult=4,
        )

    def set_item(self, text__item):
        self.ids.field.text = text__item
        self.menu.dismiss()

    # FOR DATE PICKER
    def on_save(self, instance, value, date_range):
        self.selected_date = str(value)
        print(self.selected_date)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker(min_date=datetime.date.today(),
                                   max_date=datetime.datetime.strptime("2025:05:30", '%Y:%m:%d').date(),)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def save_items(self):
        if self.selected_date != '':
            conn = sqlite3.connect('./assets/data/app_data.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT id FROM accounts WHERE status ="active"')
            uid = cursor.fetchone()

            cursor.execute(f'SELECT * FROM cart WHERE usr_id = {uid[0]}')
            rows = cursor.fetchall()
            cursor.execute('CREATE TABLE IF NOT EXISTS pending(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, usr_id, '
                           'product_id, name, price, count, size, date, res_id)')

            res_id = ''
            for i in range(10):
                res_id = res_id + str(random.randint(0, 9))

            for row in rows:
                insert = 'INSERT INTO pending(usr_id, product_id, name, price, count, size, date, res_id) ' \
                         'VALUES (?,?,?,?,?,?,?,?)'
                cursor.execute(insert, (row[1], row[2], row[3], row[4], row[6], row[7], self.selected_date, res_id))
                conn.commit()

            cursor.execute(f'DELETE from cart WHERE usr_id = {uid[0]}')
            conn.commit()
            cursor.close()
            conn.close()
            conn = sqlite3.connect(f'./assets/data/queue_{datetime.date.today()}.db')
            cursor = conn.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS AM(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,  res_id, date)')
            cursor.execute(f'CREATE TABLE IF NOT EXISTS PM(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,  res_id, date)')
            if self.ids.field.text == 'MORNING':
                cursor.execute(f'INSERT INTO AM(res_id, date) VALUES ({res_id}, "{self.selected_date}")')
            elif self.ids.field.text == 'AFTERNOON':
                cursor.execute(f'INSERT INTO PM(res_id, date) VALUES ({res_id}, "{self.selected_date}")')

            conn.commit()
            conn.close()

            self.success()

    def success(self):
        dialog = AKAlertDialog(
            header_icon="check-circle-outline", header_bg=get_color_from_hex('#FEDBD0'),
        )
        content = Factory.SuccessDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()


class Cart(Screen):
    dialog = None

    def __init__(self, **kwargs):
        super(Cart, self).__init__(**kwargs)

        self.get = MDApp.get_running_app()

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Select Date",
                type="custom",
                content_cls=ConfirmDialog(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda _: self.dialog.dismiss()
                    )]
            )

        self.dialog.open()

    def on_enter(self, *args):
        data_items = self.store_direct()

        async def on_enter():
            for info in data_items:
                await asynckivy.sleep(0)

                reserve_widgets = CartCard(index=info[0], product_id=info[2], name=info[3], price=info[4],
                                           stocks=info[5], count=info[6], size_item=info[7], category=info[8])

                self.ids.content.add_widget(reserve_widgets)

        asynckivy.start(on_enter())

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute('CREATE TABLE IF NOT EXISTS cart(id integer unique primary key autoincrement, usr_id, '
                       'product_id, name, price, stocks, count, size, category)')
        cursor.execute(f'SELECT * FROM cart WHERE usr_id = {uid[0]}')

        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)

        return data_items  # data_items

    def on_leave(self, *args):
        self.ids.content.clear_widgets()