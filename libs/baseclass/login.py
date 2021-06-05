import sqlite3
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

Builder.load_file('./libs/kv/login.kv')

class Login(Screen):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        rows = None
        try:
            conn = sqlite3.connect('./assets/data/app_data.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT password FROM accounts WHERE email = "{self.usr_name.text}"')
            rows = cursor.fetchone()
        except (AttributeError, sqlite3.OperationalError):
            rows = None

        if rows is not None:

            if self.usr_pass.text == rows[0]:
                cursor.execute(f'UPDATE accounts set status = "active" WHERE email = "{self.usr_name.text}"')
                conn.commit()
                self.reset_field()
                return True
            else:
                pass
        else:
            pass

        self.reset_field()
        conn.close()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

