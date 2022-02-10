from contextlib import asynccontextmanager

from Wordle.Game import Game
from Wordle.Lock import LockNotFoundError
from Wordle.Store.InMemory import InMemoryLock
from Wordle.Store.Store import (
    GameNotAddedError, StoreType, GameNotFoundError, GameNotUpdatedError)


class InMemoryStore():
    def __init__(self):
        self.games: dict = {}
        self.store_type: StoreType = StoreType.EPHEMERAL

    @property
    def type_desc(self) -> str:
        return self.store_type.value

    @asynccontextmanager
    async def lock(self, server_id: int, channel_id: int) -> InMemoryLock:
        if not self.games.get(server_id, {}).get(channel_id, {}).get('lock'):
            raise LockNotFoundError()

        async with self.games[server_id][channel_id]['lock']:
            yield

    async def update_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        if not self.games.get(server_id, {}).get(channel_id, {}).get('game'):
            raise GameNotUpdatedError('Game not found')

        self.games[server_id][channel_id]['game'] = game
        return game

    async def add_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        if self.games.get(server_id, {}).get(channel_id, {}).get('game'):
            raise GameNotAddedError('Game already exists')

        self.games[server_id] = self.games.get(server_id, {})
        self.games[server_id][channel_id] = {
            'game': game,
            'lock': InMemoryLock()
        }

        return game

    async def remove_game(self, server_id: int, channel_id: int) -> bool:
        try:
            self.games[server_id].pop(channel_id)
            return True
        except KeyError:
            return False

    async def get_game(self, server_id: int, channel_id: int) -> Game:
        if not self.games.get(server_id, {}).get(channel_id, {}).get('game'):
            raise GameNotFoundError()

        return self.games[server_id][channel_id]['game']
