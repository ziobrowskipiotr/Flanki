import os
import webbrowser
import re
from urllib.parse import quote
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
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
from CreateFlashcards_First import CreateFlashcards_First


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.word = None
        self.login = None
        self.subject = "Message to the developer"
        self.emails = "piotrziobrow@student.agh.edu.pl,jkrzyszczuk@student.agh.edu.pl"
        self.temp_email = None
        self.selected_file = None  # Dodano atrybut do przechowywania ścieżki do wybranego pliku
        self.words = []

    def build(self):
        Builder.load_file('LoginScreen.kv')
        Builder.load_file('RegistrationScreen.kv')
        Builder.load_file('SetLogin.kv')
        Builder.load_file('MojeKontoScreen.kv')
        Builder.load_file('MyFlashcardsScreen.kv')
        Builder.load_file('CreateFlashcardsScreen.kv')
        Builder.load_file('ImportFlashcardsScreen.kv')
        Builder.load_file('StatisticsScreen.kv')
        Builder.load_file('CreateFlashcards_First.kv')

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
        sm.add_widget(CreateFlashcards_First(name='create_flashcards_first'))

        return sm

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name

    def verify_credentials(self, login, password):
        self.login = login
        result = login_user(login, password)
        if result["success"]:
            auth_result = result["response"].get('AuthenticationResult')
            if auth_result and auth_result.get('AccessToken'):
                self.change_screen('main')
                print("Logowanie udane!")
            else:
                print("Logowanie udane, ale brak tokenu dostępu. Skontaktuj się z administratorem.")
        else:
            print(f"Logowanie nieudane! Błąd: {result['error']}")

    def register(self, first_name, last_name, email, phone_number):
        self.temp_email = email
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        phone_pattern = re.compile(r"^\d{9}$")

        if not all([first_name, last_name, email, phone_number]):
            print("Wszystkie pola muszą być wypełnione!")
        elif not email_pattern.match(email):
            print("Nieprawidłowy format adresu e-mail!")
        elif not phone_pattern.match(phone_number):
            print("Numer telefonu musi składać się z 9 cyfr!")
        else:
            self.change_screen('set_login')

    def setlogpass(self, new_login, new_password):
        email = self.temp_email
        if all([new_login, new_password, email]):
            response = register_user(new_login, new_password, email)
            if response.get('success', False):
                self.change_screen('login')
                print("Rejestracja zakończona sukcesem! Możesz się zalogować.")
            else:
                print("Nie można zarejestrować użytkownika: ", response.get('error', 'Nieznany błąd'))
        else:
            print("Wszystkie pola muszą być wypełnione!")

    def open_help_window(self):
        url = f"mailto:{self.emails}?subject={quote(self.subject)}"
        webbrowser.open(url)

    def quit_app(self):
        self.stop()

    def upload_file_to_s3(self, file_path, user_login):
        bucket_name = 'fank'
        if self.word is None:
            if len(file_path.split("/")[-1]) <= len(file_path.split("\\")[-1]):
                file_name = file_path.split("/")[-1]
            else:
                file_name = file_path.split("\\")[-1]
        else:
            file_name = self.word+".xlsx"

        print(file_name)
        print(file_name)
        print(file_name)
        print(file_name)
        print(file_name)
        print(file_name)
        print(file_name)

        object_name = f'{user_login}/{file_name}'

        s3 = boto3.client(
            's3',
            aws_access_key_id=Key.aws_access_key_id,
            aws_secret_access_key=Key.aws_secret_access_key,
            region_name=Key.region_name
        )
        try:
            # Spróbuj pobrać metadane obiektu, aby sprawdzić, czy plik już istnieje
            s3.head_object(Bucket=bucket_name, Key=object_name)
            print(f"Plik '{file_name}' już istnieje w buckecie '{bucket_name}'.")
        except ClientError as e:
            # Jeśli obiekt nie istnieje, boto3 zgłosi wyjątek ClientError. Sprawdzamy, czy to dlatego, że obiekt nie istnieje
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Plik nie istnieje, możemy bezpiecznie go przesłać
                try:
                    s3.upload_file(file_path, bucket_name, object_name)
                    print("Plik został przesłany!")
                except FileNotFoundError:
                    print("Plik nie został znaleziony.")
                except NoCredentialsError:
                    print("Błąd poświadczeń AWS.")
            else:
                # Inny błąd - coś poszło nie tak
                print(f"Nieoczekiwany błąd: {e.response['Error']['Message']}")
        if self.word is not None:
            os.remove(file_name)

    def selected(self, selection):
        self.selected_file = selection[0] if selection else None

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
        self.word = word
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
