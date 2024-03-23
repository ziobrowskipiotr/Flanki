from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class FlashcardApp(App):
    def build(self):
        # Window setup
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Logo
        self.logo = Image(source="logo.png", size_hint_y=None, height=200)
        self.window.add_widget(self.logo)

        # Buttons
        button_texts = ["Moje fiszki", "Utwórz fiszki", "Importuj fiszki", "Statystyki"]
        for text in button_texts:
            button = Button(text=text, size_hint_y=None, height=70, bold=True, background_color='#00FFCE')
            button.bind(on_press=self.callback)
            self.window.add_widget(button)

        return self.window

    def callback(self, instance):
        # Placeholder callback function
        pass

if __name__ == "__main__":
    FlashcardApp().run()