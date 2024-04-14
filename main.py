import os
import webbrowser
import re
import pandas as pd
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from urllib.parse import quote
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from openpyxl.workbook import Workbook
from MyButton import MyButton
from CreateFlashcardsScreen import CreateFlashcardsScreen
from ImportFlashcardsScreen import ImportFlashcardsScreen
from MojeKontoScreen import MojeKontoScreen
from MyFlashcardsScreen import MyFlashcardsScreen
from StatisticsScreen import StatisticsScreen
from MainScreen import MainScreen
from cognito_auth import login_user, register_user
from LoginScreen import LoginScreen
from RegistrationScreen import RegistrationScreen
from SetLogin import SetLogin
from S3_access_key import S3_key as Key
from FlashcardCreationScreen import FlashcardCreationScreen

class FlashcardsCreationScreen(Screen):
    pass

class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.word = None
        self.login = None
        self.subject = "Message to the developer"
        self.emails = "piotrziobrow@student.agh.edu.pl,jkrzyszczuk@student.agh.edu.pl"
        self.temp_email = None
        self.selected_file = None  # Dodano atrybut do przechowywania ścieżki do wybranego pliku
        self.words = []
        self.screenm = ScreenManager()
        self.fscreen = ImportFlashcardsScreen()
        screen = Screen(name="ImportFlashcardsScreen")
        screen.add_widget(self.fscreen)
        self.screenm.add_widget(screen)

    def build(self):
        Builder.load_file('LoginScreen.kv')
        Builder.load_file('RegistrationScreen.kv')
        Builder.load_file('SetLogin.kv')
        Builder.load_file('MojeKontoScreen.kv')
        Builder.load_file('MyFlashcardsScreen.kv')
        Builder.load_file('CreateFlashcardsScreen.kv')
        Builder.load_file('ImportFlashcardsScreen.kv')
        Builder.load_file('StatisticsScreen.kv')
        Builder.load_file('FlashcardCreationScreen.kv')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(SetLogin(name='set_login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MojeKontoScreen(name='moje_konto'))
        sm.add_widget(MyFlashcardsScreen(name='my_flashcards'))
        sm.add_widget(CreateFlashcardsScreen(name='create_flashcards'))
        sm.add_widget(ImportFlashcardsScreen(name='import_flashcards'))
        sm.add_widget(StatisticsScreen(name='statistics'))
        sm.add_widget(MyFlashcardsScreen(name='my_flashcards'))
        sm.add_widget(FlashcardCreationScreen(name='flashcards_creation'))


        return sm

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=5, padding=5)
        content.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint=(1, 0.25))
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))

        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def verify_credentials(self, login, password):
        print("Próba logowania z:", login)
        if not login or not password:
            self.show_popup("Błąd logowania", "Wszystkie pola muszą być uzupełnione.")
            return

        result = login_user(login, password)
        if result["success"]:
            self.login = login  # Przechowuje login użytkownika jako atrybut klasy
            self.create_user_folder_in_s3(login)  # Tworzy folder dla użytkownika w S3
            self.change_screen('main')
        else:
            self.show_popup("Błąd logowania", "Nieprawidłowy login lub hasło.")

    def create_user_folder_in_s3(self, user_login):
        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        bucket_name = 'fank'
        directory_name = f"{user_login}/"  # Nazwa folderu w S3 musi kończyć się slashem '/'

        # Sprawdzenie czy folder już istnieje
        try:
            s3.head_object(Bucket=bucket_name, Key=directory_name)
            print(f"Folder '{directory_name}' już istnieje.")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                # Folder nie istnieje, więc go tworzymy jako pusty plik zakończony slashem
                s3.put_object(Bucket=bucket_name, Key=directory_name)
                print(f"Folder '{directory_name}' został utworzony.")
            else:
                print(f"Nieoczekiwany błąd: {e}")

    def register(self, first_name, last_name, email, phone_number):
        self.temp_email = email
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        phone_pattern = re.compile(r"^\d{9}$")

        if not all([first_name, last_name, email, phone_number]):
            self.show_popup("Błąd rejestracji", "Wszystkie pola muszą być uzupełnione.")
        elif not email_pattern.match(email):
            self.show_popup("Błąd rejestracji", "Nieprawidłowy format adresu e-mail!")
        elif not phone_pattern.match(phone_number):
            self.show_popup( "Błąd rejestracji","Numer telefonu musi składać się z 9 cyfr!")
        else:
            self.change_screen('set_login')

    def setlogpass(self, new_login, new_password):
        email = self.temp_email
        if not all([new_login, new_password, email]):
            self.show_popup("Błąd rejestracji",
                            "Wszystkie pola muszą być uzupełnione.")
        elif len(new_password) < 6:
            self.show_popup("Błąd rejestracji",
                            "Hasło musi mieć co najmniej 6 liter.")
        else:
            response = register_user(new_login, new_password, email)
            if response.get('success', False):
                self.change_screen('login')
            else:
                self.show_popup("Błąd rejestracji", "Nie można zarejestrować użytkownika.")

    def open_help_window(self):
        url = f"mailto:{self.emails}?subject={quote(self.subject)}"
        webbrowser.open(url)

    def quit_app(self):
        self.stop()
    def upload_file_to_s3(self, file_path, user_login, word = None):
        bucket_name = 'fank'
        self.word = word
        if self.word is None:
            if len(file_path.split("/")[-1]) <= len(file_path.split("\\")[-1]):
                self.file_name = file_path.split("/")[-1]
            else:
                self.file_name = file_path.split("\\")[-1]
        elif self.word.endswith(".xlsx"):
            self.file_name = self.word
        else:
            self.file_name = self.word+".xlsx"

        object_name = f'{user_login}/{self.file_name}'

        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        try:
            # Spróbuj pobrać metadane obiektu, aby sprawdzić, czy plik już istnieje
            s3.head_object(Bucket=bucket_name, Key=object_name)
            print(f"Plik '{self.file_name}' już istnieje w buckecie '{bucket_name}'.")
            info_label = self.root.get_screen('import_flashcards').ids.info_label
            info_label.text = f"Plik\n'{self.file_name}'\njuż istnieje"
        except ClientError as e:
            # Jeśli obiekt nie istnieje, boto3 zgłosi wyjątek ClientError. Sprawdzamy, czy to dlatego, że obiekt nie istnieje
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Plik nie istnieje, możemy bezpiecznie go przesłać
                try:
                    s3.upload_file(file_path, bucket_name, object_name)
                    info_label = self.root.get_screen('import_flashcards').ids.info_label
                    info_label.text = f"Plik został przesłany."
                except FileNotFoundError:
                    info_label = self.root.get_screen('import_flashcards').ids.info_label
                    info_label.text = f"Plik nie został znaleziony."
                except NoCredentialsError:
                    info_label = self.root.get_screen('import_flashcards').ids.info_label
                    info_label.text = f"Błąd poświadczeń AWS."
            else:
                # Inny błąd - coś poszło nie tak
                info_label = self.root.get_screen('import_flashcards').ids.info_label
                info_label.text = "Nieoczekiwany błąd"

    def upload_selected_file(self):
        if self.selected_file:
            user_login = self.login  # Tu dodaj logikę uzyskania loginu użytkownika
            self.upload_file_to_s3(self.selected_file, user_login)
        else:
            print("Nie wybrano pliku.")

    def save_words(self, word1, word2):
        self.words.append((word1, word2))
        print("Zapisano słówka:", word1, word2)

    def save_word(self, word):
        if not word:  # Sprawdza czy wprowadzone słowo jest puste
            # Ustawia komunikat na etykiecie w bieżącym ekranie
            info_label = self.root.get_screen('create_flashcards_first').ids.info_label
            info_label.text = "Nie podano nazwy pliku."
        else:
            self.word = word
            self.change_screen('create_flashcards')  # Przechodzi do nowego ekranu tylko jeśli słowo nie jest puste
            print("Zapisano słowo:", self.word)

    def generate_excel(self):
        if not self.words:
            print("Brak danych do zapisu")
            return

        wb = Workbook()
        ws = wb.active
        ws.title = self.word

        for word_pair in self.words:
            ws.append(word_pair)

        filename = self.word+".xlsx"
        wb.save(filename)
        print(f"Plik Excel '{filename}' został wygenerowany.")
        self.upload_file_to_s3(filename, self.login)


if __name__ == '__main__':
    MainApp().run()
