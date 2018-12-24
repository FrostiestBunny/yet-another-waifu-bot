import aiohttp
import asyncio

async def get_test(url):
    result = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
    
    print(result)

loop = asyncio.get_event_loop()
# loop.run_until_complete(get_test("https://api.jikan.moe/v3/character/{}/{}".format(1, "pictures")))
loop.run_until_complete(get_test("https://api.jikan.moe/v3/search/character/?q={}".format("Maria Otonashi")))
