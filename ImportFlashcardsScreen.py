from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class ImportFlashcardsScreen(Screen, Widget):
    def on_pre_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def start_video(self):
        self.ids.video.state = 'play'

    def stop_video(self):
        self.ids.video.state = 'stop'

    def select_file(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected, filters=['*.xlsx', '*.xls'])

    def selected(self, selection):
        self.selected_file = None
        if selection:
            self.selected_file = selection[0]  # Przechowuj ścieżkę do pliku
            self.ids.bck.text = f'Wybrano plik: {self.selected_file}'  # Aktualizacja Label
            print(f"Wybrano plik: {self.selected_file}")
            if len(self.selected_file.split("/")[-1]) <= len(self.selected_file.split("\\")[-1]):
                file_name = self.selected_file.split("/")[-1]
            else:
                file_name = self.selected_file.split("\\")[-1]

            app = App.get_running_app()  # Uzyskaj obecnie działającą instancję aplikacji
            app.upload_file_to_s3(self.selected_file, app.login, file_name)  # Wywołaj metodę upload_file_to_s3
        else:
            print("Nie wybrano pliku.")


