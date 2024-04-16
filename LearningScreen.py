from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random

class LearningScreen(Screen):

    flashcards = ListProperty()  # Zdefiniowanie listy fiszek jako property Kivy

    def on_pre_enter(self):
        # Możemy teraz założyć, że flashcards są już ustawione
        self.current_index = 0
        self.update_card()

    def update_card(self):
        if self.current_index < len(self.flashcards):
            self.ids.question.text = self.flashcards[self.current_index]['front']
            self.ids.answer.text = ""  # Puste, ponieważ odpowiedź będzie pokazywana po naciśnięciu przycisku "Show Answer"

    def show_answer(self):
        self.ids.answer.text = self.flashcards[self.current_index]['back']

    def correct_answer(self):
        self.current_index += 1
        if self.current_index >= len(self.flashcards):  # Jeśli doszliśmy do końca listy
            self.end_learning_session()  # Zakończenie sesji nauki
        self.update_card()

    def wrong_answer(self):
        self.current_index += 1
        if self.current_index >= len(self.flashcards):  # Jeśli doszliśmy do końca listy
            self.end_learning_session()  # Zakończenie sesji nauki
        self.update_card()

    def end_learning_session(self):
        # Możesz tutaj dodać dodatkową logikę, np. zapis do pliku
        self.manager.current = 'main'  # Powrót do ekranu głównego