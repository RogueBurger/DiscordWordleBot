from dataclasses import dataclass


@dataclass()
class Word:
    word: str
    definition: str

    def __len__(self):
        return len(self.word)
