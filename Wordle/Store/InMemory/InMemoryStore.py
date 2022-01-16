from contextlib import asynccontextmanager
from typing import Optional


from Wordle.Game import Game
from Wordle.Lock import LockNotFoundError
from Wordle.Store.InMemory import InMemoryLock
from Wordle.Store.Store import (
    StoreType, GameNotFoundError,
    GameNotAddedError, GameNotUpdatedError)


class InMemoryStore():
    def __init__(self):
        self.games: dict = {}
        self.store_type: StoreType = StoreType.EPHEMERAL

    @property
    def type_desc(self) -> str:
        return self.store_type.value

    @asynccontextmanager
    async def lock(self, channel_id: int) -> InMemoryLock:
        try:
            async with self.games[channel_id]['lock']:
                yield
        except KeyError:
            raise LockNotFoundError()

    async def update_game(self, channel_id: int, game: Game) -> Game:
        try:
            self.games[channel_id]['game'] = game
        except KeyError:
            raise GameNotUpdatedError()

        return game

    async def add_game(self, channel_id: int, game: Game) -> Game:
        try:
            self.games[channel_id] = {
                'game': game,
                'lock': InMemoryLock()
            }
        except KeyError:
            raise GameNotAddedError

        return game

    async def remove_game(self, channel_id: int) -> bool:
        try:
            self.games.pop(channel_id)
            return True
        except KeyError:
            return False

    async def get_game(self, channel_id: int) -> Game:
        try:
            return self.games[channel_id]['game']
        except KeyError:
            raise GameNotFoundError
