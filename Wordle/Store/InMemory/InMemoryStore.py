from contextlib import asynccontextmanager

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
    async def lock(self, server_id: int, channel_id: int) -> InMemoryLock:
        try:
            async with self.games[server_id][channel_id]['lock']:
                yield
        except KeyError:
            raise LockNotFoundError()

    async def update_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        try:
            self.games[server_id][channel_id]['game'] = game
        except KeyError:
            raise GameNotUpdatedError()

        return game

    async def add_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        self.games[server_id] = self.games.get(server_id, {})

        try:
            self.games[server_id][channel_id] = {
                'game': game,
                'lock': InMemoryLock()
            }
        except KeyError:
            raise GameNotAddedError()

        return game

    async def remove_game(self, server_id: int, channel_id: int) -> bool:
        try:
            self.games[server_id].pop(channel_id)
            return True
        except KeyError:
            return False

    async def get_game(self, server_id: int, channel_id: int) -> Game:
        try:
            return self.games[server_id][channel_id]['game']
        except KeyError:
            raise GameNotFoundError()
