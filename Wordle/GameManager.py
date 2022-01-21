from contextlib import asynccontextmanager

from Wordle.Canvas import Canvas
from Wordle.Game import Game
from Wordle.Lock import Lock
from Wordle.Store import Store


class GameManager:
    def __init__(self, backend: Store):
        self.store: Store = backend
        self.canvas: Canvas = Canvas()

    def create_game(self, word_length: int, mode: str) -> Game:
        return Game(word_length=word_length, mode=mode, canvas=self.canvas)

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
        game = await self.store.get_game(channel_id)
        if not hasattr(game, 'canvas') or game.canvas is None:
            game.canvas = self.canvas

        return game

    async def stop_current_game(self, channel_id: int) -> bool:
        return await self.store.remove_game(channel_id)

    async def update_game(self, channel_id: int, game: Game) -> Game:
        """ raises GameNotUpdatedError """
        return await self.store.update_game(channel_id, game)
