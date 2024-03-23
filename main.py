from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.dropdown import DropDown


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


class FlashcardApp(App):
    def build(self):
        self.title = 'Flashcard App'
        window = BackgroundLayout()

        logo = Image(source="logo.png", size_hint=(None, None), size=(400, 200), pos_hint={'center_x': 0.5, 'top': 1})
        window.add_widget(logo)

        button_texts = ["Moje fiszki", "Utwórz fiszki", "Importuj fiszki", "Statystyki"]
        for i, text in enumerate(button_texts, start=1):
            btn = Button(text=text, size_hint=(None, None), size=(200, 50),
                         pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1})
            window.add_widget(btn)

        menu_button = Button(text='Menu', size_hint=(None, None), size=(100, 50),
                             pos_hint={'left': 1, 'top': 1})
        menu_button.bind(on_release=self.show_menu)
        window.add_widget(menu_button)

        self.menu = DropDown()
        options = ["Pomoc", "Odśwież", "Moje konto"]
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.menu.select(btn.text))
            self.menu.add_widget(btn)

        return window

    def show_menu(self, instance):
        self.menu.open(instance)


if __name__ == "__main__":
    FlashcardApp().run()