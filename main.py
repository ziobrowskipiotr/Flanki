from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle


class BackgroundLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(BackgroundLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0.1, 0.2, 0.3, 1)  # Kolor tła
            self.rect = Rectangle(size=(self.width, self.height), pos=self.pos)

        # Aby tło aktualizowało się razem z rozmiarem okna
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class FlashcardApp(App):
    def build(self):
        self.title = 'Flashcard App'
        window = BackgroundLayout()

        # Dodawanie widgetów do BackgroundLayout
        logo = Image(source="logo.png", size_hint=(None, None), size=(400, 200), pos_hint={'center_x': 0.5, 'top': 1})
        window.add_widget(logo)

        button_texts = ["Moje fiszki", "Utwórz fiszki", "Importuj fiszki", "Statystyki"]
        for i, text in enumerate(button_texts, start=1):
            btn = Button(text=text, size_hint=(None, None), size=(200, 50),
                         pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1})
            window.add_widget(btn)

        return window


if __name__ == "__main__":
    FlashcardApp().run()