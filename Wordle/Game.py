import sqlite3
from contextlib import closing

from Helpers.RandomText import RandomText


class Game:
    CORRECT = 'correct'
    INCORRECT = 'incorrect'
    INVALID = 'invalid'

    def __init__(self, word_length=5):
        self.word_length: int = word_length
        self.num_guesses: int = 0
        self.target: str = ''
        self.con = sqlite3.connect('words.db')

        self.generate_target()

    def generate_target(self):
        with closing(self.con.cursor()) as cur:
            cur.execute(
                'SELECT word, LENGTH(word) FROM words WHERE LENGTH(word)=? ORDER BY RANDOM() LIMIT 1',
                (self.word_length,)
            )
            result = cur.fetchone()
            self.target = result[0]

    def guess(self, word) -> tuple:
        lowered_word = word.lower()
        if not word or len(word) != self.word_length:
            return self.INVALID, f'Your guesses must be {self.word_length} letters long.'

        if lowered_word == self.target:
            return self.CORRECT, f'{word} is the correct answer! Congrats!'

        if not self.word_exists(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot()}'

        return self.INCORRECT, f'That is incorrect: {self.format_word(word)}'

    def word_exists(self, word):
        with closing(self.con.cursor()) as cur:
            cur.execute('SELECT id FROM words WHERE word=?', (word,))
            if cur.fetchone():
                return True

        return False

    def format_word(self, word):
        return ' '.join([self.format_letter(letter.lower(), index) for index, letter in enumerate(word)])

    def format_letter(self, letter, index):
        if self.target[index] == letter:
            return chr(ord(letter) + 127215)

        if letter in self.target:
            return chr(ord(letter) + 9301)

        return letter.capitalize()
