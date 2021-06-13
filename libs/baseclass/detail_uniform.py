import sqlite3
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.utils import asynckivy
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder

Builder.load_file('./libs/kv/detail_uniform.kv')

class DetailCard(MDCard):
    image = StringProperty('')
    name = StringProperty('')
    price = StringProperty('')
    description = StringProperty('')
    brand = StringProperty('')
    count = NumericProperty(0)
    stocks = NumericProperty(0)

    def reserve(self):
        get = MDApp.get_running_app()
        conn = sqlite3.connect('./assets/data/app_data.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS reservations(id integer unique primary key autoincrement, '
                       'category, product_id, count, products, price)')
        insert = 'INSERT INTO reservations (usr_id, store_id, product_id, count, products, price) VALUES (?,?,?,?,?,?)'
        cursor.execute(insert, (id_usr[0], get.store_index, get.product_index, self.count, self.name, self.price))
        conn.commit()
        conn.close()
        Reservation().open()

class ProductDetails(Screen):
    def __init__(self, **kwargs):
        super(ProductDetails, self).__init__(**kwargs)
        self.get = get = MDApp.get_running_app()

    def on_enter(self):
        data_items = []
        conn = data_base.conn_db(f'./assets/data/pcerve_data.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM store_{self.get.store_index} where id = {self.get.product_index}")
        rows = cursor.fetchone()
        cursor.close()
        conn.close()

        for row in rows:
            data_items.append(row)

        async def on_enter():
            await asynckivy.sleep(0)
            details = DetailCard(image=f'./assets/{self.get.store_index}/{data_items[0]}.jpg', name=data_items[1],
                                 description=data_items[3], brand=data_items[5], price=str(data_items[2]),
                                 stocks=data_items[6])
            self.ids.content.add_widget(details)

        asynckivy.start(on_enter())

        # self.image = f'./assets/{store_index}/{data_items[0]}.jpg'
        # self.name = data_items[1]

    def on_pre_leave(self, *args):
        self.ids.content.clear_widgets()

class Reservation(ModalView):
    pass
