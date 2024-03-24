import webbrowser

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class BackgroundLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(BackgroundLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0.1, 0.2, 0.3, 1)  # Kolor tła
            self.rect = Rectangle(size=(self.width, self.height), pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MyFlashcardsWindow(Popup):
    def __init__(self, **kwargs):
        super(MyFlashcardsWindow, self).__init__(**kwargs)

        self.title = "Moje fiszki"

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        back_button = Button(text='Powrót', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_release=self.dismiss)
        layout.add_widget(back_button)
    pass


class CreateFlashcardsWindow(Popup):
    def __init__(self, **kwargs):
        super(CreateFlashcardsWindow, self).__init__(**kwargs)

        self.title = "Utwórz fiszki"

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        back_button = Button(text='Powrót', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_release=self.dismiss)
        layout.add_widget(back_button)
    pass


class ImportFlashcardsWindow(Popup):
    def __init__(self, **kwargs):
        super(ImportFlashcardsWindow, self).__init__(**kwargs)

        self.title = "Importuj fiszki"

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        back_button = Button(text='Powrót', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_release=self.dismiss)
        layout.add_widget(back_button)
    pass


class StatisticsWindow(Popup):
    def __init__(self, **kwargs):
        super(StatisticsWindow, self).__init__(**kwargs)

        self.title = "Statystyki"

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        back_button = Button(text='Powrót', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_release=self.dismiss)
        layout.add_widget(back_button)
    pass


class MyAccountWindow(Popup):
    def __init__(self, **kwargs):
        super(MyAccountWindow, self).__init__(**kwargs)

        self.title = "Moje konto"

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        back_button = Button(text='Powrót', size_hint=(None, None), size=(100, 50))
        back_button.bind(on_release=self.dismiss)
        layout.add_widget(back_button)
    pass

class FlashcardApp(App):
    def build(self):
        self.title = 'Flashcard App'
        window = BackgroundLayout()

        logo = Image(source="logo.png", size_hint=(None, None), size=(400, 200), pos_hint={'center_x': 0.5, 'top': 1})
        window.add_widget(logo)

        button_texts = ["Moje fiszki", "Utwórz fiszki", "Importuj fiszki", "Statystyki"]
        button_actions = [self.open_my_flashcards_window, self.open_create_flashcards_window,
                          self.open_import_flashcards_window, self.open_statistics_window]
        for i, (text, action) in enumerate(zip(button_texts, button_actions), start=1):
            btn = Button(text=text, size_hint=(None, None), size=(200, 50),
                         pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1})
            btn.bind(on_release=action)
            window.add_widget(btn)

        menu_button = Button(text='Menu', size_hint=(None, None), size=(100, 50),
                             pos_hint={'left': 1, 'top': 1})
        menu_button.bind(on_release=self.show_menu)
        window.add_widget(menu_button)

        self.menu = DropDown()
        options = ["Pomoc", "Moje konto", "Odśwież"]
        options_actions = [self.open_help_window, self.open_myaccount_window, self.open_refresh_window]
        for option, action in zip(options, options_actions):
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn, action=action: action())
            self.menu.add_widget(btn)

        return window

    def show_menu(self, instance):
        self.menu.open(instance)

    def open_my_flashcards_window(self, instance):
        my_flashcards_window = MyFlashcardsWindow()
        my_flashcards_window.open()

    def open_create_flashcards_window(self, instance):
        create_flashcards_window = CreateFlashcardsWindow()
        create_flashcards_window.open()

    def open_import_flashcards_window(self, instance):
        import_flashcards_window = ImportFlashcardsWindow()
        import_flashcards_window.open()

    def open_statistics_window(self, instance):
        statistics_window = StatisticsWindow()
        statistics_window.open()

    def open_help_window(self):
        webbrowser.open("https://www.youtube.com/watch?v=6gNpSuE01qE&t=317s")

    def open_refresh_window(self):
        Clock.schedule_once(self.restart_app)

    def restart_app(self, dt):
        self.stop()
        new_app_instance = FlashcardApp()
        new_app_instance.run()

    def open_myaccount_window(self):
        myaccount_window = MyAccountWindow()
        myaccount_window.open()



if __name__ == "__main__":
    FlashcardApp().run()
