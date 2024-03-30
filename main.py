from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
import numpy as np

class GradientBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            texture = self.create_gradient_texture([0, 1, 0, 1], [1, 0, 0, 1])
            Rectangle(size=self.size, pos=self.pos, texture=texture)

    def create_gradient_texture(self, start_color, end_color, resolution=(1024, 1)):
        data = np.zeros((resolution[0], 4), dtype=np.float32)
        for i in range(resolution[0]):
            current_color = np.array(start_color) * (1 - i / resolution[0]) + np.array(end_color) * (i / resolution[0])
            data[i] = current_color
        texture = Texture.create(size=resolution, colorfmt='rgba')
        texture.blit_buffer(data.flatten().tobytes(), colorfmt='rgba', bufferfmt='float')
        return texture

class MainApp(App):
    def build(self):
        return Builder.load_file('flanki.kv')

if __name__ == '__main__':
    MainApp().run()
