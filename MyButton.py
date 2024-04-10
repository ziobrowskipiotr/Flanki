from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button


class MyButton(Button):
    def change_color(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0, 1)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[self.height / 2.2, ])