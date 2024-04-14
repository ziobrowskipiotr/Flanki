import os
import boto3
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from S3_access_key import S3_key as Key
from botocore.exceptions import NoCredentialsError, ClientError
class CreateFlashcardsScreen(Screen):
    def create_new_flashcard_folder(self):
        app = App.get_running_app()
        user_login = app.login
        new_folder_name = self.ids.folder_name_input.text

        if not new_folder_name:
            app.show_popup("Error", "Nie podano nazwy folderu.")
            return

        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        bucket_name = 'fank'
        directory_name = f"{user_login}/{new_folder_name}/"

        try:
            s3.head_object(Bucket=bucket_name, Key=directory_name)
            print(f"Folder '{directory_name}' już istnieje.")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                s3.put_object(Bucket=bucket_name, Key=directory_name)
                print(f"Folder '{directory_name}' został utworzony.")
            else:
                print(f"Nieoczekiwany błąd: {e}")

        app.root.current = 'flashcards_creation'
        app.current_folder = directory_name


    def on_pre_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def start_video(self):
        self.ids.video.state = 'play'

    def stop_video(self):
        self.ids.video.state = 'stop'

    def create(self):
        self.create_new_flashcard_folder()
        app = App.get_running_app()
        app.generate_excel()
        os.remove(app.file_name)
