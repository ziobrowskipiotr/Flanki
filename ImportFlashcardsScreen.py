import re

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import pandas as pd
import os
import s3fs
from S3_access_key import S3_key as Key


def clean_filename(filename):
    """Cleans and truncates filenames to be filesystem-safe."""
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename[:100]


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
            self.selected_file = selection[0]
            self.ids.bck.text = f'Selected file: {self.selected_file}'
            print(f"Selected file: {self.selected_file}")

            app = App.get_running_app()
            user_folder = f"{app.login}/"

            df = pd.read_excel(self.selected_file, header=None)

            if df.shape[1] < 2:
                print("Error: The file does not have enough columns.")
                return

            for index, row in df.iterrows():
                front, back = row[0], row[1]
                filename = f"{clean_filename(front)}-{clean_filename(back)}.xlsx"
                s3_path = f"s3://{Key.bucket_name}/{user_folder}{filename}"
                df_flashcard = pd.DataFrame([[front, back]])
                self.write_df_to_excel_s3(df_flashcard, s3_path)
        else:
            print("No file selected.")

    def write_df_to_excel_s3(self, df, s3_path):
        s3 = s3fs.S3FileSystem(anon=False,
            key=Key.aws_access_key_id,
            secret=Key.aws_secret_access_key,
            client_kwargs={'region_name': Key.region_name})
        with s3.open(s3_path, 'wb') as f:
            with pd.ExcelWriter(f, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
                print(f"Flashcard created and uploaded: {s3_path}")
