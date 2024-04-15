import pandas as pd
import s3fs
from kivy.app import App
from kivy.uix.screenmanager import Screen
from S3_access_key import S3_key as Key

class FlashcardCreationScreen(Screen):
    def save_flashcard(self):
        front_text = self.ids.front_card.text
        back_text = self.ids.back_card.text
        if not front_text or not back_text:
            App.get_running_app().show_popup("Error", "Nie podano treści fiszki.")
            return

        # Utworzenie DataFrame bez nagłówków kolumn
        df = pd.DataFrame([[front_text, back_text]])

        filename = f"{front_text}.xlsx"
        s3_path = f"s3://{Key.bucket_name}/{App.get_running_app().current_folder}{filename}"

        self.write_df_to_excel_s3(df, s3_path)
        print(f"Fiszka zapisana w pliku {s3_path}.")
        self.ids.front_card.text = ""
        self.ids.back_card.text = ""

    def write_df_to_excel_s3(self, df, file_path):
        s3 = s3fs.S3FileSystem(anon=False,
                               key=Key.aws_access_key_id,
                               secret=Key.aws_secret_access_key,
                               client_kwargs={'region_name': Key.region_name})

        with s3.open(file_path, 'wb') as f:
            # Użycie ExcelWriter do zapisu DataFrame bez nagłówków kolumn
            with pd.ExcelWriter(f, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)

    def on_pre_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def start_video(self):
        self.ids.video.state = 'play'

    def stop_video(self):
        self.ids.video.state = 'stop'
