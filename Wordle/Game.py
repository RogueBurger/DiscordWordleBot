from Helpers.RandomText import RandomText
from Wordle.Words import Words


class Game:
    CORRECT = 'correct'
    INCORRECT = 'incorrect'
    INVALID = 'invalid'

    def __init__(self, word_length: int = 5):
        self.word_length: int = word_length
        self.num_guesses: int = 0
        self.target: str = ''
        self.definition: str = ''
        self.guesses: list = []

        self.generate_target()

    def generate_target(self):
        self.target, self.definition = Words.get_random_word(self.word_length)

        print(f'New game started: "{self.target}"')

    def guess(self, word: str) -> tuple:
        lowered_word = word.lower()
        if not word or len(word) != self.word_length:
            # TODO: something else should probably be in charge of generating these responses
            return self.INVALID, f'Your guesses must be {self.word_length} letters long.'

        if lowered_word == self.target:
            return self.CORRECT, f'{word} is the correct answer! Congrats! {word}: {self.definition}'

        if not Words.get_word(lowered_word):
            return self.INVALID, f'{word} is not a word, you {RandomText.idiot()}'

        formatted_word = self.__format_word(word)
        self.guesses.append(formatted_word)

        return self.INCORRECT, f'That is incorrect: {formatted_word}'

    def get_history(self) -> list:
        return self.guesses

    def __format_word(self, word: str) -> str:
        return ' '.join([self.__format_letter(letter.lower(), index) for index, letter in enumerate(word)])

    def __format_letter(self, letter: str, index: int) -> str:
        if self.target[index] == letter:
            return chr(ord(letter) + 127215)

        if letter in self.target:
            return chr(ord(letter) + 9301)

        return letter.capitalize()
