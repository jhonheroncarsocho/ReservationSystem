import sqlite3
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

Builder.load_file('./libs/kv/login.kv')

class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        try:
            conn = sqlite3.connect('./assets/data/app_data.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT password FROM accounts WHERE email = "{self.usr_name.text}"')
            rows = cursor.fetchone()
            conn.close()
        except (AttributeError, sqlite3.OperationalError):
            rows = None

        if rows is not None:

            if self.usr_pass.text == rows[0]:
                conn = sqlite3.connect('./assets/data/app_data.db')
                cursor = conn.cursor()
                cursor.execute(f'UPDATE accounts set status = "active" WHERE email = "{self.usr_name.text}"')
                conn.commit()
                conn.close()
                self.reset_field()
                return True
            else:
                print('Wrong Email or Password')
        else:
            print('Wrong Email or Password')

        self.reset_field()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

