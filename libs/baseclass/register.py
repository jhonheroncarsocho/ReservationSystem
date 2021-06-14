import sqlite3
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

Builder.load_file('./libs/kv/register.kv')

class Register(Screen):
    usr_name = ObjectProperty(None)
    usr_email = ObjectProperty(None)
    usr_pass1 = ObjectProperty(None)
    usr_pass2 = ObjectProperty(None)

    def register(self):
        if self.usr_name.text != '' or self.usr_pass1.text != '' or self.usr_pass2.text != '' \
                or self.usr_email.text != '':

            if self.usr_pass1.text == self.usr_pass2.text:
                conn = sqlite3.connect('./assets/data/app_data.db')
                cursor = conn.cursor()

                cursor.execute('CREATE TABLE IF NOT EXISTS accounts(id integer unique primary key autoincrement, name, '
                               'email, password, status)')
                insert_query = 'INSERT INTO accounts (name, email, password) VALUES (?,?,?)'
                cursor.execute(insert_query, (self.usr_name.text, self.usr_email.text, self.usr_pass1.text))
                conn.commit()
                conn.close()

                self.reset_field()
                # manage.current = 'login'
                return True
            else:
                self.error2()
                self.reset_field()

        else:
            self.error3()
            return False

    def reset_field(self):
        self.usr_name.text = ''
        self.usr_email.text = ''
        self.usr_pass1.text = ''
        self.usr_pass2.text = ''

    def error2(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorDialog2()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def error3(self):
        dialog = AKAlertDialog(
            header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
        )
        content = Factory.ErrorDialog3()
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()
        