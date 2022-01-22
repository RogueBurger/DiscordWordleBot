import string
from typing import Optional

from Helpers.RandomText import RandomText
from Wordle.Word import Word
from Wordle.Words import Words
from Wordle.Canvas import Canvas, Image, Glyph, GlyphColor


class Game:
    CORRECT: str = 'correct'
    INCORRECT: str = 'incorrect'
    INVALID: str = 'invalid'
    FAILED: str = 'failed'

    EASY: str = 'easy'
    LIMITED: str = 'limited'
    PUZZLE: str = 'puzzle'

    def __init__(self, mode: str, word_length: int = 5, canvas: Optional[Canvas] = None):
        self.target: Optional[Word] = None
        self.mode: str = mode
        self.canvas: Canvas = canvas
        self.guesses: list = []
        self.progress: Optional[Image] = None

        self.generate_target(word_length=word_length, mode=mode)

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state['canvas']
        return state

    def generate_target(self, word_length: int, mode: str):
        if mode == Game.PUZZLE:
            targets = Words.get_random(word_length, word_length + 1)
            self.target = targets[0]
            self.guesses = [word.word for word in targets[1:]]
            for guess in self.guesses:
                drawn_word = self.draw_word(guess)
                self.progress = self.canvas.vertical_join(
                    self.progress, drawn_word) if self.progress else drawn_word
        else:
            self.target = Words.get_random(word_length)[0]

    def suggest(self):
        return Words.get_random(len(self.target))[0].word

    def guess(self, word: str, author_id: int) -> tuple:
        if not word or len(word) != len(self.target):
            return self.INVALID, f'Your guesses must be {len(self.target)} letters long.', None

        lowered_word = word.lower()

        if lowered_word != self.target.word and self.mode != self.PUZZLE and not Words.get_by_word(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot(author_id)}', None

        drawn_word = self.draw_word(lowered_word)

        if lowered_word not in self.guesses:
            self.guesses.append(lowered_word)
            self.progress = self.canvas.vertical_join(
                self.progress, drawn_word) if self.progress else drawn_word

        if lowered_word == self.target.word:
            if self.mode == Game.PUZZLE:
                return self.CORRECT, \
                    f'{RandomText.success()} \n' \
                    f'The word was {word}.\n' \
                    f'*{word}*: {self.target.definition}', \
                    self.progress

            return self.CORRECT, \
                f'{RandomText.success()} {word.capitalize()} is the correct answer!' \
                f'It took you {len(self.guesses)} {self.get_guess_word(len(self.guesses))}.\n' \
                f'*{word}*: {self.target.definition}', \
                self.progress

        if self.mode in [self.LIMITED, self.PUZZLE] and len(self.guesses) > len(self.target):
            return self.FAILED, \
                f'{RandomText.failure()}\n' \
                f'The correct answer is {self.target.word}. ' \
                f'*{self.target.word}*: {self.target.definition}', \
                drawn_word

        if self.mode in [self.LIMITED, self.INCORRECT]:
            remaining: int = len(self.target) - len(self.guesses) + 1
            return self.INCORRECT, \
                f'Incorrect. You have {remaining} {self.get_guess_word(remaining)} left.', \
                drawn_word

        return self.INCORRECT, None, drawn_word

    def get_unused_letters(self):
        letters = list(string.ascii_lowercase)
        for word in self.guesses:
            for letter in word:
                letters.remove(letter) if letter in letters else None
        return self.canvas.draw_word([self.canvas.draw_char(letter.upper(), GlyphColor.COLD) for letter in letters])

    def get_history(self) -> list:
        return self.guesses

    def draw_word(self, word):
        return self.canvas.draw_word([self.draw_letter(letter) for letter in self.check_word(word)])

    def draw_letter(self, letter) -> Glyph:
        if letter['status'] == self.CORRECT:
            return self.canvas.draw_char(letter['letter'].upper(), GlyphColor.HOT)

        if letter['status'] == self.INCORRECT:
            return self.canvas.draw_char(letter['letter'].upper(), GlyphColor.WARM)

        return self.canvas.draw_char(letter['letter'].upper(), GlyphColor.COLD)

    def check_word(self, word):
        target_map: list = [None if letter == word[i]
                            else letter for i, letter in enumerate(self.target.word)]
        guess_map: list = [
            {'letter': letter, 'status': None} if target_map[i] else {
                'letter': letter, 'status': self.CORRECT}
            for i, letter in enumerate(word)
        ]

        for i, letter in enumerate(guess_map):
            if letter['status'] == self.CORRECT:
                continue

            if letter['letter'] in target_map:
                target_map[target_map.index(letter['letter'])] = None
                guess_map[i]['status'] = self.INCORRECT
                continue

            guess_map[i]['status'] = self.INVALID

        return guess_map

    @staticmethod
    def get_guess_word(count: int) -> str:
        return 'guess' if count == 1 else 'guesses'
