import asyncio
import secrets
from collections.abc import Awaitable, Callable


def to_async[R, **P](func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def secrets_choice(seq: str, n: int) -> str:
    return "".join([secrets.choice(seq) for _ in range(n)])
