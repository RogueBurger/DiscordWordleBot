from asyncio import Lock

from Wordle.Lock import LockError


class InMemoryLock(Lock):
    async def __aexit__(self, *args):
        return await self.release()

    async def release(self):
        return super().release()

    async def acquire(self, **kwargs) -> bool:
        return await super().acquire()

    async def extend(self, **kwargs) -> bool:
        if await super().acquire():
            return self
        raise LockError()
