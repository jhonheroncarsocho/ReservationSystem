import sqlite3
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

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
        if self.usr_name == '' or self.usr_pass == '':
            self.error()

        else:
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
                    self.error()
            else:
                self.error()

            self.reset_field()

    def error(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorDialog()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_pass.text = ''

