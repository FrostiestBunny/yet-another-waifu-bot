import asyncio
import aiohttp
import os


GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
GITHUB_API_URL = "https://api.github.com/"
USER_AGENT = "User-Agent: yet-another-waifu-bot"
CUSTOM_ACCEPT = "application/vnd.github.inertia-preview+json"
PROJECT_ID = "2029170"
COLUMN_ID = "4039174"


async def create_card(body):
    body = body.strip('*')
    url = GITHUB_API_URL + "projects/columns/" + COLUMN_ID + "/cards"
    params = {
        'access_token': GITHUB_API_TOKEN
    }
    headers = {
        'Accept': CUSTOM_ACCEPT
    }
    payload = {
        'note': body
    }
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, params=params, headers=headers) as resp:
            response = await resp.json()
