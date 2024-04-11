import os

from kivy.app import App
from kivy.uix.screenmanager import Screen


class CreateFlashcards_First(Screen):
    def on_pre_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def start_video(self):
        self.ids.video.state = 'play'

    def stop_video(self):
        self.ids.video.state = 'stop'

