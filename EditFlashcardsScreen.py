import os
import tempfile
import subprocess
import boto3
import s3fs
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from openpyxl import load_workbook
from io import BytesIO
from S3_access_key import S3_key as Key


class EditFlashcardsScreen(Screen):

    def on_pre_enter(self):
        self.load_folders()

    def load_folders(self):
        app = App.get_running_app()
        user_login = app.login
        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        bucket_name = 'fank'
        prefix = f"{user_login}/"
        result = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')

        folders = result.get('CommonPrefixes')
        self.ids.folders_box.clear_widgets()
        if folders:
            for folder in folders:
                folder_name = folder.get('Prefix')[len(prefix):-1]
                btn = Button(text=folder_name, size_hint_y=None, height=40)
                btn.bind(on_release=lambda x, folder=folder_name: self.show_flashcards(folder))
                self.ids.folders_box.add_widget(btn)
        else:
            self.show_popup("Informacja", "Nie ma takiego folderu.")

    def show_flashcards(self, folder_name):
        app = App.get_running_app()
        user_login = app.login
        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        bucket_name = 'fank'
        prefix = f"{user_login}/{folder_name}/"
        result = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        flashcards = [obj['Key'] for obj in result.get('Contents', []) if obj['Key'].endswith('.xlsx')]

        self.ids.files_box.clear_widgets()
        for file_key in sorted(flashcards):
            base_name = os.path.basename(file_key)
            file_index = int(base_name.split('.')[0])
            formatted_name = f"{file_index:03}.xlsx"
            btn = Button(text=formatted_name, size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, fk=f"s3://{bucket_name}/{file_key}": self.edit_flashcard(fk))
            self.ids.files_box.add_widget(btn)

    def edit_flashcard(self, s3_path):
        local_path = self.download_and_open_excel(s3_path)
        self.current_local_path = local_path
        self.current_s3_path = s3_path

    def download_and_open_excel(self, s3_path):
        s3 = s3fs.S3FileSystem(anon=False,
                               key=Key.aws_access_key_id,
                               secret=Key.aws_secret_access_key,
                               client_kwargs={'region_name': Key.region_name})

        local_path = os.path.join(tempfile.gettempdir(), os.path.basename(s3_path))
        with s3.open(s3_path, 'rb') as f:
            with open(local_path, 'wb') as local_file:
                local_file.write(f.read())

        self.open_excel(local_path)
        return local_path

    def open_excel(self, path):
        if os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            subprocess.call(['open', path])

    def upload_to_s3(self, local_path, s3_path):
        s3 = s3fs.S3FileSystem(anon=False,
                               key=Key.aws_access_key_id,
                               secret=Key.aws_secret_access_key,
                               client_kwargs={'region_name': Key.region_name})

        with open(local_path, 'rb') as f:
            with s3.open(s3_path, 'wb') as s3_file:
                s3_file.write(f.read())

        print(f"Plik {os.path.basename(s3_path)} został przesłany z powrotem do S3.")

    def save_changes(self):
        if hasattr(self, 'current_local_path') and hasattr(self, 'current_s3_path'):
            self.upload_to_s3(self.current_local_path, self.current_s3_path)
            self.clear_flashcards_view()
            self.show_popup("Udane", "Fiszka została edytowana")
        else:
            self.show_popup("Błąd", "Coś poszło nie tak.")

    def clear_flashcards_view(self):
        self.ids.files_box.clear_widgets()
        self.load_folders()

    def show_popup(self, title, message):
        window_width = Window.width
        window_height = Window.height

        content = BoxLayout(orientation='vertical', spacing=5, padding=5)
        content.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint=(1, 0.25))
        content.add_widget(close_btn)

        popup_width = min(400, window_width * 0.8)
        popup_height = min(200, window_height * 0.5)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(popup_width, popup_height))

        close_btn.bind(on_press=popup.dismiss)

        popup.open()
