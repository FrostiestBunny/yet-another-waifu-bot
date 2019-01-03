import aiohttp


class HTTPSession:

    def __init__(self):
        self.http_session = None

    def connect(self):
        self.http_session = aiohttp.ClientSession()
    
    def get_connection(self):
        return self.http_session
    
    async def close(self):
        await self.http_session.close()


http_session = HTTPSession()
