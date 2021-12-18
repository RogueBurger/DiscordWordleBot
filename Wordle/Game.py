from typing import Optional

from Helpers.RandomText import RandomText
from Wordle.Words import Words
from Wordle.Canvas import Canvas, Image, Glyph, GlyphColor


class Game:
    CORRECT: str = 'correct'
    INCORRECT: str = 'incorrect'
    INVALID: str = 'invalid'

    def __init__(self, canvas: Canvas, word_length: int = 5):
        self.word_length: int = word_length
        self.num_guesses: int = 0
        self.target: str = ''
        self.definition: str = ''
        self.guesses: list = []
        self.progress: Optional[Image] = None
        self.canvas: Canvas = canvas

        self.generate_target()

    def generate_target(self):
        self.target, self.definition = Words.get_random_word(self.word_length)

        print(f'New game started: "{self.target}"')

    def guess(self, word: str) -> tuple:
        lowered_word = word.lower()
        if not word or len(word) != self.word_length:
            return self.INVALID, f'Your guesses must be {self.word_length} letters long.', None

        if lowered_word == self.target:
            return self.CORRECT, \
                   f'{word} is the correct answer! Congrats! {word}: {self.definition}', \
                   self.draw_word(word)

        if not Words.get_word(lowered_word):
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
        if self.target[index] == letter:
            return self.canvas.draw_char(letter.upper(), GlyphColor.HOT)

        if letter in self.target:
            return self.canvas.draw_char(letter.upper(), GlyphColor.WARM)

        return self.canvas.draw_char(letter.upper(), GlyphColor.COLD)
