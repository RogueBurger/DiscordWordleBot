from contextlib import asynccontextmanager

from Wordle.Game import Game
from Wordle.Lock import Lock
from Wordle.Store import Store


class GameManager:
    def __init__(self, backend: Store):
        self.store: Store = backend

    @asynccontextmanager
    async def lock(self, channel_id: int) -> Lock:
        """ raises LockNotFoundError """
        async with self.store.lock(channel_id):
            yield

    async def add_game(self, channel_id: int, game: Game) -> Game:
        """ raises GameNotAddedError """
        return await self.store.add_game(channel_id, game)

    async def get_current_game(self, channel_id: int) -> Game:
        """ raises GameNotFoundError """
        return await self.store.get_game(channel_id)

    async def stop_current_game(self, channel_id: int) -> bool:
        return await self.store.remove_game(channel_id)

    async def update_game(self, channel_id: int, game: Game) -> Game:
        """ raises GameNotUpdatedError """
        return await self.store.update_game(channel_id, game)
