async def print_(string: str) -> None:
    print(string)

async def main():
    strings = ['Enjoy', 'Rosetta','Code','Whole','Lot']
    coroutines = map(print_, strings)
    await asyncio.gather(*coroutines) #START


def run_async_code():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


if __name__ == '__main__':
    run_async_code()
