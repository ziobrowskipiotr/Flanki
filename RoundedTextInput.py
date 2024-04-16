from kivy.graphics import RoundedRectangle, Color
from kivy.uix.textinput import TextInput


class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(RoundedTextInput, self).__init__(**kwargs)
        # Ustawienia graficzne, które zostaną zastosowane przed rysowaniem widgetu
        with self.canvas.before:
            Color(1, 1, 1, 0.5)  # Biały kolor z półprzezroczystością
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        # Uaktualnij rysunek przy każdej zmianie pozycji lub rozmiaru widgetu
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size