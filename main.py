import webbrowser

from kivy.app import App
from kivy.lang import Builder
# *** Important importing!!! ***
from MyButton import MyButton
from CreateFlashcardsScreen import CreateFlashcardScreen
from ImportFlashcardsScreen import ImportFlashcardsScreen
from MojeKontoScreen import MojeKontoScreen
from MyFlashcardsScreen import MyFlashcardsScreen
from StatisticsScreen import StatisticsScreen
from MainScreen import MainScreen
# *** end ***


class MainApp(App):
    def build(self):
        # Załaduj najpierw definicje dla poszczególnych ekranów
        Builder.load_file('MojeKontoScreen.kv')
        Builder.load_file('MyFlashcardsScreen.kv')
        Builder.load_file('CreateFlashcardsScreen.kv')
        Builder.load_file('ImportFlashcardsScreen.kv')
        Builder.load_file('StatisticsScreen.kv')
        # Następnie załaduj główny plik .kv, który korzysta z tych ekranów
        return Builder.load_file('main.kv')

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name

    def open_help_window(self):
        webbrowser.open("https://www.youtube.com/watch?v=6gNpSuE01qE&t=317s")


    def restart_app(self):
        self.stop()
        new_app_instance = MainApp()
        new_app_instance.run()


if __name__ == '__main__':
    MainApp().run()
