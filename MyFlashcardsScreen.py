import boto3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from openpyxl import load_workbook
from io import BytesIO
from kivy.uix.screenmanager import Screen
class MyFlashcardsScreen(Screen):
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
                folder_name = folder.get('Prefix').strip(prefix).strip('/')
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

        all_cards_content = ""
        if 'Contents' in result:
            for file in result['Contents']:
                file_name = file['Key'].split('/')[-1]
                if file_name.endswith('.xlsx'):
                    response = s3.get_object(Bucket=bucket_name, Key=file['Key'])
                    file_content = response['Body'].read()
                    wb = load_workbook(filename=BytesIO(file_content))
                    ws = wb.active
                    for row in ws.iter_rows(values_only=True):
                        all_cards_content += f"{row[0]} - {row[1]}\n" if len(row) > 1 else f"{row[0]}\n"

        if all_cards_content:
            self.display_cards(all_cards_content)
        else:
            self.show_popup("Informacja", "W folderze nie ma żadnych fiszek")

    def display_cards(self, cards_content):
        content_label = Label(text=cards_content, size_hint_y=None, height=400)
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(content_label)

        box_layout = BoxLayout(orientation='vertical')
        box_layout.add_widget(scroll_view)
        close_button = Button(text="Close", size_hint=(1, None), height=50)
        close_button.bind(on_release=lambda x: popup.dismiss())

        box_layout.add_widget(close_button)
        popup = Popup(title="Flashcard Details", content=box_layout, size_hint=(None, None), size=(420, 500))
        popup.open()

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=5, padding=5)
        content.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint=(1, 0.25))
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))

        close_btn.bind(on_press=popup.dismiss)

        popup.open()