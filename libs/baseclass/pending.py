import sqlite3
import datetime
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.utils import asynckivy
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

Builder.load_file('./libs/kv/pending.kv')


class PendingCard(MDCard):
    res_id = StringProperty('')
    date = StringProperty('')
    q_number = NumericProperty(0)
    time_pick = StringProperty()

    def delete_item(self):
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()
        cursor.execute(f'DELETE from pending where res_id = {self.res_id} and usr_id = {uid[0]}')
        conn.commit()
        conn.close()
        conn = sqlite3.connect(f'./assets/data/queue_{datetime.date.today()}.db')
        cursor = conn.cursor()

        uid = cursor.fetchone()
        cursor.execute(f'DELETE from {self.time_pick} where res_id = {self.res_id}')
        conn.commit()
        conn.close()
        self.parent.remove_widget(self)
        Snackbar(text='Order is cancelled')

    def view_receipt(self):
        open_receipt = ViewReceipt(res_id=self.res_id)
        open_receipt.open()


class ReceiptCard(MDCard):
    index = NumericProperty()
    name = StringProperty()
    price = StringProperty()
    count = NumericProperty()
    size_uniform = StringProperty('')
    date = StringProperty()


class ViewReceipt(MDDialog):
    res_id = StringProperty()
    total_price = NumericProperty()

    def on_open(self):
        data_items = self.store_direct()
        print(data_items)

        total_price = 0
        for info in data_items:
            x = info[4].replace(",", "")
            total_price += float(x)

            reserve_widgets = ReceiptCard(index=info[0], name=f'{info[3]}', price=info[4],
                                            count=info[5], size_uniform=info[6], date=info[7])

            self.ids.dialog_content.add_widget(reserve_widgets)
        self.total_price = total_price

    def store_direct(self):
        data_items = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()
        print(self.res_id)
        cursor.execute(f'SELECT * FROM pending WHERE res_id = "{self.res_id}"')

        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data_items.append(row)

        return data_items  # data_items

    def close_receipt(self):
        self.dismiss()


class Pending(Screen):
    def __init__(self, **kwargs):
        super(Pending, self).__init__(**kwargs)

        self.get = MDApp.get_running_app()

    def on_enter(self, *args):
        res_ids = self.store_direct()

        async def on_enter():
            for info in res_ids:
                await asynckivy.sleep(0)

                conn = sqlite3.connect(f'./assets/data/queue_{datetime.date.today()}.db')
                cursor = conn.cursor()

                cursor.execute(
                    f'CREATE TABLE IF NOT EXISTS AM(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,  res_id, date)')
                cursor.execute(
                    f'CREATE TABLE IF NOT EXISTS PM(id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,  res_id, date)')

                cursor.execute(f'SELECT id, date FROM AM WHERE res_id = {info[0]}')
                id_AM = cursor.fetchone()

                cursor.execute(f'SELECT id, date FROM PM WHERE res_id = {info[0]}')
                id_PM = cursor.fetchone()

                if id_AM is not None:
                    reserve_widgets = PendingCard(res_id=info[0], q_number=id_AM[0], time_pick='AM', date=id_AM[1])
                    self.ids.content.add_widget(reserve_widgets)

                elif id_PM is not None:
                    reserve_widgets = PendingCard(res_id=info[0], q_number=id_PM[0], time_pick="PM", date=id_PM[1])
                    self.ids.content.add_widget(reserve_widgets)

                conn.close()
        asynckivy.start(on_enter())

    def store_direct(self):
        res_id = []
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM accounts WHERE status = "active"')
        uid = cursor.fetchone()

        cursor.execute('CREATE TABLE IF NOT EXISTS pending(id integer unique primary key autoincrement, usr_id, '
                       'product_id, name, price, count, size, date, res_id)')
        cursor.execute(f'SELECT res_id FROM pending WHERE usr_id = {uid[0]}')

        rows = cursor.fetchall()
        conn.close()
        for i in rows:
            if i not in res_id:
                res_id.append(i)

        return res_id  # data_items

    def on_leave(self, *args):
        self.ids.content.clear_widgets()
