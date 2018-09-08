import asyncio

# Instagram
def wait_for(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

# result = wait_for(async_func())
