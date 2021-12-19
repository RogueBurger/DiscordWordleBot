from typing import Optional

from Wordle.Game import Game


class GameManager:
    def __init__(self):
        self.games: dict = {}

    def add_game(self, channel_id: int, game: Game) -> Game:
        self.games[channel_id] = game
        return game

    def get_current_game(self, channel_id: int) -> Optional[Game]:
        try:
            return self.games[channel_id]
        except KeyError:
            return None

    def stop_current_game(self, channel_id: int) -> bool:
        try:
            self.games.pop(channel_id)
            return True
        except KeyError:
            return False
