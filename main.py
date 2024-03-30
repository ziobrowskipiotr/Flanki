from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup


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
