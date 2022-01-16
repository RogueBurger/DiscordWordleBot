import pickle

from contextlib import asynccontextmanager

from Wordle.Game import Game
from Wordle.Lock import Lock
from Wordle.RedisClient import RedisClient
from Wordle.Store import (
    StoreType, GameNotFoundError,
    GameNotAddedError, GameNotUpdatedError)


class RedisStore():
    def __init__(self, client: RedisClient):
        self.client: RedisClient = client
        self.path_prefix: str = self.client.path('wordle')
        self.store_type: StoreType = StoreType.PERSISTENT

    @property
    def type_desc(self) -> str:
        return self.store_type.value

    @asynccontextmanager
    async def lock(self, channel_id: int) -> Lock:
        async with self.client.lock(
                self.client.path(self.path_prefix, 'lock', channel_id),
                timeout=5,
                blocking_timeout=10):

            yield

    async def get_game(self, channel_id: int) -> Game:
        pickled_game = await self.client.get(
            self.client.path(self.path_prefix, 'game', channel_id))

        if pickled_game:
            return pickle.loads(pickled_game)

        raise GameNotFoundError()

    async def _set_game(self,
                        channel_id: str,
                        game: Game,
                        only_if_new: bool = False,
                        must_exist: bool = False) -> bool:

        return await self.client.set(
            name=self.client.path(self.path_prefix, 'game', channel_id),
            value=pickle.dumps(game),
            nx=only_if_new,
            xx=must_exist)

    async def update_game(self, channel_id: str, game: Game) -> Game:
        if await self._set_game(
                channel_id=channel_id, game=game, must_exist=True):

            return game

        raise GameNotUpdatedError()

    async def add_game(self, channel_id: str, game: Game) -> Game:
        if await self._set_game(
                channel_id=channel_id, game=game, only_if_new=True):

            return game

        raise GameNotAddedError()

    async def remove_game(self, channel_id: int) -> bool:
        return await self.client.delete(
            self.client.path(self.path_prefix, 'game', channel_id)) == 1
