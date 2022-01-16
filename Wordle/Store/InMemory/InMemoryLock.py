from asyncio import Lock

from Wordle.Lock import LockError


class InMemoryLock(Lock):
    async def acquire(self, **kwargs) -> bool:
        return await super().acquire()

    async def extend(self, **kwargs) -> bool:
        if await super().acquire():
            return self
        raise LockError()
