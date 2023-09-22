import asyncio
import functools
import time

def track_speed(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        coro = func(*args, **kwargs)
        task = asyncio.ensure_future(coro)
        await task
        execution_time = time.time() - start_time
        print(f"Execution time for {func.__name__}: {execution_time} seconds")
        return task.result()
    return wrapper
