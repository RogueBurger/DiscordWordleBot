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

    def __init__(self, canvas: Canvas, mode: str, word_length: int = 5):
        self.canvas: Canvas = canvas
        self.target: Word = self.generate_target(word_length)
        self.mode = mode
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
                self.draw_word(lowered_word)

        if not Words.get_by_word(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot()}', None

        drawn_word = self.draw_word(lowered_word)
        if lowered_word not in self.guesses:
            self.guesses.append(lowered_word)
            self.progress = self.canvas.vertical_join(self.progress, drawn_word) if self.progress else drawn_word

        if self.mode == self.LIMITED and len(self.guesses) > len(self.target):
            return self.FAILED, \
                f'You have run out of guesses. The correct answer is {self.target.word}. ' \
                f'*{self.target.word}*: {self.target.definition}', \
                drawn_word
        if self.mode == self.LIMITED and self.INCORRECT:
            return self.INCORRECT, f'Incorrect. You have {len(self.target) - len(self.guesses) + 1} guesses left.', drawn_word

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
        target_map: list = [None if letter == word[i] else letter for i, letter in enumerate(self.target.word)]
        guess_map: list = [
            {'letter': letter, 'status': None} if target_map[i] else {'letter': letter, 'status': self.CORRECT}
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
