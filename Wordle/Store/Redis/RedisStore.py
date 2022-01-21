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

    def path(self, server_id: int, channel_id: int, key: str):
        return self.client.path(
            self.path_prefix, 'server', server_id, 'channel', channel_id, key)

    @ asynccontextmanager
    async def lock(self, server_id: int, channel_id: int) -> Lock:
        async with self.client.lock(
                self.path(server_id, channel_id, 'lock'),
                timeout=5,
                blocking_timeout=10):

            yield

    async def get_game(self, server_id: int, channel_id: int) -> Game:
        pickled_game = await self.client.get(
            self.path(server_id, channel_id, 'game'))

        if pickled_game:
            return pickle.loads(pickled_game)

        raise GameNotFoundError()

    async def _set_game(self,
                        server_id: int,
                        channel_id: int,
                        game: Game,
                        only_if_new: bool = False,
                        must_exist: bool = False) -> bool:

        return await self.client.set(
            name=self.path(server_id, channel_id, 'game'),
            value=pickle.dumps(game),
            nx=only_if_new,
            xx=must_exist)

    async def update_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        if await self._set_game(
                server_id=server_id,
                channel_id=channel_id,
                game=game,
                must_exist=True):
            return game

        raise GameNotUpdatedError()

    async def add_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        if await self._set_game(
                server_id=server_id,
                channel_id=channel_id,
                game=game,
                only_if_new=True):
            return game
        raise GameNotAddedError()

    async def remove_game(self, server_id: int, channel_id: int) -> bool:
        return await self.client.delete(
            self.path(server_id, channel_id, 'game')) == 1
