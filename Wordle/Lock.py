from typing import Protocol


class LockError(Exception):
    ...


class LockNotFoundError(LockError):
    ...


class LockNotOwnedError(LockError):
    ...


class Lock(Protocol):
    def __aenter__(self):
        ...

    def __aexit__(self, *args):
        ...

    async def acquire(self, **kwargs) -> bool:
        ...

    async def release(self) -> bool:
        ...

    async def extend(self, **kwargs):
        ...
