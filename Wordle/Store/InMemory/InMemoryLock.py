import asyncio


class InMemoryLock(asyncio.Lock):
    async def __aexit__(self, *args):
        return await self.release()

    async def release(self):
        return super().release()

    async def acquire(self, **kwargs) -> bool:
        try:
            return await asyncio.wait_for(
                super().acquire(),
                timeout=kwargs.get('timeout'))
        except asyncio.TimeoutError:
            return False

    async def extend(self, **kwargs) -> bool:
        if await self.acquire(**kwargs):
            return True
        return False
