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
    return response


async def create_gist(desc, body):
    url = GITHUB_API_URL + "gists"
    params = {
        'access_token': GITHUB_API_TOKEN
    }
    headers = {
        'Accept': CUSTOM_ACCEPT
    }
    payload = {
        'description': desc,
        'files': {
            'waifus.txt': {
                'content': body
            }
        }
    }
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, params=params, headers=headers) as resp:
            response = await resp.json()
    return response


async def get_gist(gist_id):
    url = GITHUB_API_URL + "gists/" + str(gist_id)
    params = {
        'access_token': GITHUB_API_TOKEN
    }
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            response = await resp.json()
    return response


async def update_gist(gist_id, body):
    url = GITHUB_API_URL + "gists/" + str(gist_id)
    params = {
        'access_token': GITHUB_API_TOKEN
    }
    headers = {
        'Accept': CUSTOM_ACCEPT
    }
    payload = {
        'files': {
            'waifus.txt': {
                'content': body
            }
        }
    }
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, params=params, headers=headers) as resp:
            response = await resp.json()
    return response


async def get_commits():
    url = GITHUB_API_URL + "repos/zackunfair/yet-another-waifu-bot/commits"
    params = {
        'access_token': GITHUB_API_TOKEN
    }
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            response = await resp.json()
    
    return response
