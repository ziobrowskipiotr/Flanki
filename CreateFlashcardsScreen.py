import os

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class CreateFlashcardsScreen(Screen):
    def on_pre_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def start_video(self):
        self.ids.video.state = 'play'

    def stop_video(self):
        self.ids.video.state = 'stop'

    def create(self):
        app = App.get_running_app()  # Uzyskaj obecnie działającą instancję aplikacji
        app.generate_excel()
        os.remove(app.file_name)