from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from gui import Ui_MainWindow
from paint import HangmanCanvas
import random

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window for the Hangman game. Handles UI setup, game logic, and user interactions.
    """
    def __init__(self) -> None:
        """
        Sets up the UI and hangman drawing, connects all buttons, and creates all variables
        for the game logic to work
        """
        super().__init__()
        self.setupUi(self)

        self.canvas: HangmanCanvas = HangmanCanvas()
        layout: QVBoxLayout = QVBoxLayout(self.drawingArea)
        layout.addWidget(self.canvas)
        self.canvas.update()

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            button = getattr(self, f'button_{letter}')
            button.clicked.connect(lambda _, l=letter: self.guess(l))
            button.setVisible(False)

        self.button_playagain.clicked.connect(lambda: self.start_game(self.difficulty))
        self.button_change_difficulty.clicked.connect(lambda: self.change_difficulty())
        self.button_difficulty_easy.clicked.connect(lambda: self.start_game('easy'))
        self.button_difficulty_medium.clicked.connect(lambda: self.start_game('medium'))
        self.button_difficulty_hard.clicked.connect(lambda: self.start_game('hard'))

        self.button_change_difficulty.setVisible(False)
        self.button_playagain.setVisible(False)

        self.gameover_label.lower()
        self.numguesses_label.setText('')
        self.bestscore_label.setText('')

        self.difficulty: str = 'easy'
        self.top_score: int = 0
        self.num_guesses: int = 6
        self.guesses: list[str] = []
        self.correct_guesses: list[str] = []
        self.word_to_guess: str = ''
        self.current_guess: list[str] = []

    def get_random_word(self) -> str:
        """
        Sees which words haven't been guessed yet and returns a random one
        :return: Returns a random word that hasn't been correctly guessed yet
        """
        try:
            if self.difficulty == 'easy':
                with open('easy_words.txt', 'r') as file:
                    words: list[str] = [line.strip() for line in file]
            elif self.difficulty == 'medium':
                with open('medium_words.txt', 'r') as file:
                    words: list[str] = [line.strip() for line in file]
            elif self.difficulty == 'hard':
                with open('hard_words.txt', 'r') as file:
                    words: list[str] = [line.strip() for line in file]
        except FileNotFoundError:
            print(f"Word list file for difficulty '{self.difficulty}' not found.")

        valid_words: list[str] = [word for word in words if word not in self.correct_guesses]

        if not valid_words:
            self.correct_guesses.clear()
            valid_words = words

        return random.choice(valid_words)

    def draw_body_part(self) -> None:
        """
        Tells the painter what need to be drawn after a guess is done
        """
        match self.num_guesses:
            case 6:
                self.canvas.add_body_part("gallows")
            case 5:
                self.canvas.add_body_part("head")
            case 4:
                self.canvas.add_body_part("body")
            case 3:
                self.canvas.add_body_part("leftarm")
            case 2:
                self.canvas.add_body_part("rightarm")
            case 1:
                self.canvas.add_body_part("leftleg")
            case 0:
                self.canvas.add_body_part("rightleg")

    def guess(self, guess: str) -> None:
        """
        Handles what happens when the user guesses a letter
        If the guess is correct, updates the word
        If the guess is incorrect, take away a guess and draw a body part
        :param guess: The letter the user guessed
        """
        if self.num_guesses > 0:
            try:
                getattr(self, f'button_{guess}').setEnabled(False)
            except AttributeError:
                print(f"Button for letter '{guess}' not found")
            if guess in self.word_to_guess:
                self.guesses.append(guess)
                for i, char in enumerate(self.word_to_guess):
                    if char in self.guesses:
                        self.current_guess[i] = char
                self.guess_label.setText(''.join(self.current_guess))
                if ''.join(self.current_guess) == self.word_to_guess:
                    self.top_score = self.num_guesses
                    self.num_guesses = 0
                    self.game_over(True)
            else:
                self.num_guesses -= 1
                self.numguesses_label.setText(f'Guesses: {self.num_guesses}')
                self.draw_body_part()
                if self.num_guesses == 0:
                    self.game_over(False)

    def start_game(self, difficulty: str) -> None:
        """
        Resets all game logic to start the game
        :param difficulty: The difficulty level of the game (easy, medium, or hard)
        """
        self.difficulty = difficulty
        self.num_guesses = 6
        self.word_to_guess = self.get_random_word().lower()
        self.current_guess = ['_' for _ in self.word_to_guess]
        self.guesses = []

        self.button_playagain.setVisible(False)
        self.button_change_difficulty.setVisible(False)
        self.button_difficulty_easy.setVisible(False)
        self.button_difficulty_medium.setVisible(False)
        self.button_difficulty_hard.setVisible(False)
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            try:
                getattr(self, f'button_{letter}').setEnabled(True)
                getattr(self, f'button_{letter}').setVisible(True)
            except AttributeError:
                print(f"Button for letter '{letter}' not found")

        self.guess_label.setText('_' * len(self.word_to_guess))
        self.gameover_label.setText('')
        self.difficulty_label.setText('')
        self.numguesses_label.setText(f'Guesses: {self.num_guesses}')
        self.bestscore_label.setText(f'Best: {self.top_score}')

        self.draw_body_part()

    def change_difficulty(self) -> None:
        """
        Shows the difficulty screen to allow the user to pick a different difficulty
        """
        self.button_difficulty_easy.setVisible(True)
        self.button_difficulty_medium.setVisible(True)
        self.button_difficulty_hard.setVisible(True)
        self.button_playagain.setVisible(False)
        self.button_change_difficulty.setVisible(False)

        self.gameover_label.setText('')
        self.numguesses_label.setText('')
        self.bestscore_label.setText('')
        self.difficulty_label.setText('Choose a difficulty')

    def game_over(self, won: bool) -> None:
        """
        Shows the gameover screen with options to play again or change the difficulty
        :param won: True if the player won, False otherwise
        """
        self.button_playagain.setVisible(True)
        self.button_change_difficulty.setVisible(True)
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            getattr(self, f'button_{letter}').setVisible(False)

        if won:
            self.correct_guesses.append(self.word_to_guess)

        self.canvas.reset_drawing()

        self.gameover_label.setText(f'{'YOU WIN' if won else 'YOU LOSE'}\nThe word was {self.word_to_guess}')
        self.guess_label.setText('')
        self.numguesses_label.setText('')
        self.bestscore_label.setText('')

