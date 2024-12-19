async def main():
    strings = ['Enjoy', 'Rosetta','Code','Whole','Lot']
    async def print_(string: str) -> None:
        print(string)
    coroutines = map(print_, strings)
    await asyncio.gather(*coroutines) #START


if __name__ == '__main__':
    asyncio.run(main())
