async def print_(string: str) -> None:
    print(string)

async def main():
    strings = ['Enjoy', 'Rosetta']
    coroutines = map(print_, strings)
    await asyncio.gather(*coroutines)
    #START

if __name__ == '__main__':
    asyncio.run(main())