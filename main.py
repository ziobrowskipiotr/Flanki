import webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from MyButton import MyButton
from CreateFlashcardsScreen import CreateFlashcardsScreen
from ImportFlashcardsScreen import ImportFlashcardsScreen
from MojeKontoScreen import MojeKontoScreen
from MyFlashcardsScreen import MyFlashcardsScreen
from StatisticsScreen import StatisticsScreen
from MainScreen import MainScreen
class LoginScreen(Screen):
    pass

class RegistrationScreen(Screen):
    pass

class SetLogin(Screen):
    pass
class MainApp(App):
    def build(self):
        Builder.load_file('login_screen.kv')
        Builder.load_file('registration_screen.kv')
        Builder.load_file('set_login.kv')
        Builder.load_file('MojeKontoScreen.kv')
        Builder.load_file('MyFlashcardsScreen.kv')
        Builder.load_file('CreateFlashcardsScreen.kv')
        Builder.load_file('ImportFlashcardsScreen.kv')
        Builder.load_file('StatisticsScreen.kv')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(SetLogin(name='set_login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MojeKontoScreen(name='moje_konto'))
        sm.add_widget(MyFlashcardsScreen(name='my_flashcards'))
        sm.add_widget(CreateFlashcardsScreen(name='create_flashcards'))
        sm.add_widget(ImportFlashcardsScreen(name='import_flashcards'))
        sm.add_widget(StatisticsScreen(name='statistics'))

        return sm

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name

    def verify_credentials(self, login, password):
        if login and password:
            self.change_screen('main')
        else:
            print("Wszystkie pola muszą być wypełnione!")

    def register(self, first_name, last_name, email, phone_number):
        if all([first_name, last_name, email, phone_number]):
            self.change_screen('set_login')
        else:
            print("Wszystkie pola muszą być wypełnione!")

    def setlogpass(self, new_login, new_password):
        if all([new_login, new_password]):
            self.change_screen('login')
        else:
            print("Wszystkie pola muszą być wypełnione!")

    def open_help_window(self):
        webbrowser.open("https://www.youtube.com/watch?v=6gNpSuE01qE&t=317s")

    def quit_app(self):
        self.stop()

if __name__ == '__main__':
    MainApp().run()
