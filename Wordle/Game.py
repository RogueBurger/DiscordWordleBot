from typing import Optional

from Helpers.RandomText import RandomText
from Wordle.Word import Word
from Wordle.Words import Words
from Wordle.Canvas import Canvas, Image, Glyph, GlyphColor


class Game:
    CORRECT: str = 'correct'
    INCORRECT: str = 'incorrect'
    INVALID: str = 'invalid'

    def __init__(self, canvas: Canvas, word_length: int = 5):
        self.canvas: Canvas = canvas
        self.target: Word = self.generate_target(word_length)
        self.guesses: list = []
        self.num_guesses: int = 0
        self.progress: Optional[Image] = None

    @staticmethod
    def generate_target(word_length):
        target = Words.get_random(word_length)

        if target:
            print(f'New game started: "{target.word}"')

        return target

    def guess(self, word: str) -> tuple:
        lowered_word = word.lower()
        if not word or len(word) != len(self.target):
            return self.INVALID, f'Your guesses must be {len(self.target)} letters long.', None

        if lowered_word == self.target.word:
            guess_word: str = 'guess' if len(self.guesses) == 0 else 'guesses'
            return self.CORRECT, \
                f'{word} is the correct answer! Congrats! ' \
                f'It took you {len(self.guesses) + 1} {guess_word}.\n' \
                f'*{word}*: {self.target.definition}', \
                self.draw_word(word)

        if not Words.get_by_word(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot()}', None

        drawn_word = self.draw_word(word)
        if lowered_word not in self.guesses:
            self.guesses.append(lowered_word)
            self.progress = self.canvas.vertical_join(self.progress, drawn_word) if self.progress else drawn_word

        return self.INCORRECT, None, drawn_word

    def get_history(self) -> list:
        return self.guesses

    def draw_word(self, word):
        return self.canvas.draw_word([self.draw_letter(letter.lower(), index) for index, letter in enumerate(word)])

    def draw_letter(self, letter, index) -> Glyph:
        if self.target.word[index] == letter:
            return self.canvas.draw_char(letter.upper(), GlyphColor.HOT)

        if letter in self.target.word:
            return self.canvas.draw_char(letter.upper(), GlyphColor.WARM)

        return self.canvas.draw_char(letter.upper(), GlyphColor.COLD)
