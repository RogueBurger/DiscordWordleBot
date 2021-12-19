import os
import sqlite3
from contextlib import closing


# TODO: Refactor this into more of true model, instead of one-off static methods
from typing import Optional

from Wordle.Word import Word


class Words:
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATABASE: str = os.path.join(BASE_DIR, "../wordle.db")
    WORDLIST: str = os.path.join(BASE_DIR, "../wordlist.txt")

    @staticmethod
    def create_db():
        with open(Words.DATABASE, "w"):
            con = sqlite3.connect(Words.DATABASE)
            with closing(con.cursor()) as cur:
                cur.execute('''
                    CREATE TABLE words (
                        word CHAR(25) NOT NULL,
                        definition VARCHAR(255) NOT NULL  
                    );
                ''')
            con.commit()

    @staticmethod
    def seed():
        con = sqlite3.connect(Words.DATABASE)
        with closing(con.cursor()) as cur:
            with open(Words.WORDLIST) as wordlist:
                for line in wordlist:
                    try:
                        word, definition = line.split('	')
                        cur.execute('INSERT INTO words VALUES(?,?)', (word.lower(), definition))
                    except ValueError:
                        continue
        con.commit()

    @staticmethod
    def get_by_word(word: str) -> list[Word]:
        con = sqlite3.connect(Words.DATABASE)
        with closing(con.cursor()) as cur:
            cur.execute(
                'SELECT word, definition FROM words WHERE word=?',
                (word.lower(),)
            )
            return [Words.__hydrate_word(row[0], row[1]) for row in cur.fetchall()]

    @staticmethod
    def get_random(word_length: int = 5) -> Optional[Word]:
        con = sqlite3.connect(Words.DATABASE)
        with closing(con.cursor()) as cur:
            cur.execute(
                'SELECT word, definition FROM words '
                'WHERE LENGTH(word)=? ORDER BY RANDOM() LIMIT 1',
                (word_length,)
            )
            row = cur.fetchone()
            return Words.__hydrate_word(row[0], row[1]) if row else None

    @staticmethod
    def __hydrate_word(word: str, definition: str) -> Word:
        return Word(word, definition.replace('\n', '').strip())
