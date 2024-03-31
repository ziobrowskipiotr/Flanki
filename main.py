from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from MyButton import MyButton  # Zaimportuj swój niestandardowy przycisk


class MainScreen(Screen):
    pass


class MojeKontoScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        # Załaduj najpierw definicje dla poszczególnych ekranów
        Builder.load_file('MojeKontoScreen.kv')
        # Następnie załaduj główny plik .kv, który korzysta z tych ekranów
        return Builder.load_file('main.kv')

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name
        else:
            print(f"Ekran '{screen_name}' nie istnieje.")


if __name__ == '__main__':
    MainApp().run()
