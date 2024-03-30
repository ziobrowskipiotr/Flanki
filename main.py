from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.button import Button


class MyButton(Button):
    def change_color(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 0, 1)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[self.height / 2.2, ])


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = None

    def build(self):
        return Builder.load_file('flanki.kv')

if __name__ == '__main__':
    MainApp().run()
