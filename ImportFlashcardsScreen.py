from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import pandas as pd
import os
import s3fs
from S3_access_key import S3_key as Key

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
            self.selected_file = selection[0]  # Store the file path
            self.ids.bck.text = f'Selected file: {self.selected_file}'  # Update Label
            print(f"Selected file: {self.selected_file}")

            file_name = os.path.basename(self.selected_file)
            base_name = os.path.splitext(file_name)[0]

            app = App.get_running_app()  # Get the currently running app instance
            user_folder = f"{app.login}/{base_name}/"  # Define user folder path

            # Read Excel file
            df = pd.read_excel(self.selected_file, header=None)  # Assume no header row

            # Check if the DataFrame is in expected format
            if df.shape[1] < 2:
                print("Error: The file does not have enough columns.")
                return

            # Process each row in the DataFrame
            for index, row in df.iterrows():
                front, back = row[0], row[1]
                flashcard_file = f"{user_folder}{index+1:03d}.xlsx"
                self.create_flashcard(flashcard_file, front, back)

        else:
            print("No file selected.")

    def create_flashcard(self, file_path, front, back):
        """Create a flashcard file and upload it to S3."""
        df_flashcard = pd.DataFrame({'Front': [front], 'Back': [back]})
        s3_path = f"s3://{Key.bucket_name}/{file_path}"

        s3 = s3fs.S3FileSystem(anon=False,
                               key=Key.aws_access_key_id,
                               secret=Key.aws_secret_access_key,
                               client_kwargs={'region_name': Key.region_name})
        with s3.open(s3_path, 'wb') as f:
            with pd.ExcelWriter(f, engine='openpyxl') as writer:
                df_flashcard.to_excel(writer, index=False, header=False)
        print(f"Flashcard created and uploaded: {s3_path}")
