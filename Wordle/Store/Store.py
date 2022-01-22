from contextlib import asynccontextmanager
from enum import Enum
from typing import Optional, Protocol

from Wordle.Game import Game
from Wordle.Lock import Lock


class StoreType(Enum):
    EPHEMERAL = 'ephemeral'
    PERSISTENT = 'persistent'


class StoreError(Exception):
    ...


class GameNotAddedError(StoreError):
    ...


class GameNotUpdatedError(StoreError):
    ...


class GameNotFoundError(StoreError):
    ...


class Store(Protocol):
    @property
    def type_desc(self) -> str:
        ...

    @asynccontextmanager
    def lock(self, server_id: int, channel_id: int) -> Lock:
        ...

    def update_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        ...

    def add_game(self, server_id: int, channel_id: int, game: Game) -> Game:
        ...

    def remove_game(self, server_id: int, channel_id: int) -> bool:
        ...

    async def get_game(self, server_id: int, channel_id: int) -> Game:
        ...
