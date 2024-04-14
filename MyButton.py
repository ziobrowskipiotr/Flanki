from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ListProperty

def darken_color(color, amount=0.8):
    """ Zmniejsza jasność koloru o podany procent (domyślnie o 20%). """
    return [max(0, c * amount) for c in color[:-1]] + [color[-1]]  # Nie zmieniaj alfa

class MyButton(Button):
    bgc_create = ListProperty([173/255, 216/255, 230/255, 1])
    bgc_import = ListProperty([255/255, 105/255, 180/255, 1])
    bgc_my = ListProperty([156/255, 235/255, 189/255, 1])
    bgc_edit = ListProperty([147/255, 112/255, 219/255, 1])
    background_down_color = ListProperty(darken_color([173/255, 216/255, 230/255, 1], 0.5))  # Tutaj ciemniejszy o 50%
