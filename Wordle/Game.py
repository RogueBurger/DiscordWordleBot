import string
import json
from typing import Dict, Optional
from operator import indexOf

from Helpers.RandomText import RandomText
from Wordle.Word import Word
from Wordle.Words import Words
from Wordle.Canvas import Canvas, Image
from Wordle.Canvas.Glyph import GlyphColor, GlyphShape


class Game:
    CORRECT: str = 'correct'
    INCORRECT: str = 'incorrect'
    INVALID: str = 'invalid'
    FAILED: str = 'failed'

    EASY: str = 'easy'
    LIMITED: str = 'limited'
    PUZZLE: str = 'puzzle'

    CHAR_WHITELIST = []

    def __init__(self, mode: str, word_length: int = 5, canvas: Optional[Canvas] = None):
        self.target: Optional[Word] = None
        self.mode: str = mode
        self.canvas: Canvas = canvas
        self.guesses: list = []
        self.progress: Optional[Image] = None
        self.limit: int = self.get_limit_for_length(word_length)
        self.letter_status: Dict[str, Optional[str]] = {
            letter: None for letter in string.ascii_lowercase}
        self.target_progress: list[Optional[str]] = [None] * word_length

        self.generate_target(word_length=word_length, mode=mode)

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state['canvas']
        return state

    def generate_target(self, word_length: int, mode: str):
        if mode == Game.PUZZLE:
            targets = Words.get_random(word_length, self.limit)
            self.target = targets[0]
            self.guesses = [word.word for word in targets[1:]]
            self.progress = self.canvas.vertical_join(
                images=[self.draw_word(guess) for guess in self.guesses])
        else:
            self.target = Words.get_random(word_length)[0]

    def suggest(self):
        return Words.get_random(len(self.target))[0].word

    def guess(self, word: str, author_id: int) -> tuple:
        if not word or len(word) != len(self.target):
            return self.INVALID, f'Your guesses must be {len(self.target)} letters long.', None

        lowered_word = word.lower()

        if any(letter for letter in lowered_word if letter not in string.ascii_lowercase):
            return self.INVALID, f'{word} contains illegal characters, you {RandomText.idiot(author_id)}', None

        if lowered_word != self.target.word and self.mode != self.PUZZLE and not Words.get_by_word(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot(author_id)}', None

        image = self.draw_word(lowered_word)

        if lowered_word not in self.guesses:
            self.guesses.append(lowered_word)
            self.progress = self.canvas.vertical_join(
                images=list(filter(None, [self.progress, image])))

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

        if self.mode in [self.LIMITED, self.PUZZLE] and len(self.guesses) >= self.limit:
            return self.FAILED, \
                f'{RandomText.failure()}\n' \
                f'The correct answer is {self.target.word}. ' \
                f'*{self.target.word}*: {self.target.definition}', \
                image

        if self.mode in [self.LIMITED, self.INCORRECT]:
            remaining: int = self.limit - len(self.guesses)
            return self.INCORRECT, \
                f'Incorrect. You have {remaining} {self.get_guess_word(remaining)} left.', \
                image

        return self.INCORRECT, None, image

    def draw_unused_letters(self):
        rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

        words = [[(letter.upper(), self.status_color(self.letter_status[letter]))
                  for letter in row] for row in rows]

        # Insert a blank character to shift the bottom row left
        words[2].append((' ', GlyphColor.CLEAR))

        return self.canvas.vertical_join([
            self.canvas.draw_word(word=word, shape=GlyphShape.WIDE) for word in words])

    def draw_known_letters(self):
        return self.canvas.draw_word(
            word=[(letter.upper(), self.status_color(self.CORRECT)) if letter else (
                ' ', self.status_color(self.INVALID)) for letter in self.target_progress])

    def draw_word(self, word: str):
        guess_map = self.check_word(word)

        word = [(letter['letter'].upper(), self.status_color(letter['status']))
                for letter in guess_map]

        return self.canvas.draw_word(word)

    def check_word(self, word):
        target_map: list = [None if letter == word[i]
                            else letter for i, letter in enumerate(self.target.word)]

        guess_map: list = [{'letter': letter, 'status': None} if target_map[i] else {
            'letter': letter, 'status': self.CORRECT} for i, letter in enumerate(word)]

        for i, letter in enumerate(guess_map):
            if letter['status'] == self.CORRECT:
                self.target_progress[i] = letter['letter']
                continue

            if letter['letter'] in target_map:
                target_map[target_map.index(letter['letter'])] = None
                guess_map[i]['status'] = self.INCORRECT
                continue

            guess_map[i]['status'] = self.INVALID

        for item in guess_map:
            letter = item['letter']
            status = item['status']
            existing = self.letter_status[letter]

            if existing is None:
                self.letter_status[letter] = status
                continue

            if existing == self.CORRECT:
                continue

            if status in [self.CORRECT, self.INCORRECT]:
                self.letter_status[letter] = status
                continue

        return guess_map

    def status_color(
            self,
            status: str,
            default: GlyphColor = GlyphColor.LIGHT_GRAY) -> GlyphColor:

        return {
            self.CORRECT: GlyphColor.GREEN,
            self.INCORRECT: GlyphColor.YELLOW,
            self.INVALID: GlyphColor.INVERSE_LIGHT_GRAY
        }.get(status, default)

    @staticmethod
    def get_guess_word(count: int) -> str:
        return 'guess' if count == 1 else 'guesses'

    @staticmethod
    def get_limit_for_length(length: int) -> int:
        if length < 2:
            length = 2
        if length > 15:
            length = 15

        length_to_limit = {2: 6, 3: 5, 4: 5, 5: 6, 6: 6, 7: 7,
                           8: 7, 9: 8, 10: 8, 11: 9, 12: 9, 13: 9, 14: 9, 15: 10}

        return length_to_limit[length]

    def cheat(self):
        if self.limit - len(self.guesses) > 2:
            return (
                'Whoa there, bub. At least try a *little*!'
            )
        else:
            with open("wordlist.json", "r") as f:
                word_list = json.load(f)
            
            lst_possibles = []
            must_haves = []
            forbiddens = []

            for w in self.guesses:
                for l in w:
                    if l in list(self.target.word):
                        must_haves.append(l)
                    else:
                        forbiddens.append(l)

            for i in word_list:
                if len(i) == len(self.target): # checks word length, working
                    if not any(set(i) & set(forbiddens)): # checks if forbidden letters occur, working
                        if set(must_haves).intersection(set(i)) == set(must_haves): # checks if must-have letters occur, working
                            for l in self.target_progress:
                                if (l != i[indexOf(self.target_progress,l)]) and (l != None):
                                    break
                            else:
                                lst_possibles.append(i)

            return f'Fine...here you go...*cheater!*\n```{lst_possibles}```'