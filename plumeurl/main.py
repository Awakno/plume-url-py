import aiohttp


def pyproject_getversion():
    with open("pyproject.toml", "r") as file:
        for line in file:
            if "version" in line:
                return line.split("=")[1].strip().replace('"', "")


version = pyproject_getversion()


class PlumeUrlAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://url.ptarmigan.xyz/api"
        self.version = "plume-url.js/{version}".format(version=version)
        self.api_key = api_key

    async def request(self, method, endpoint, **kwargs):
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                method,
                self.base_url + endpoint,
                headers={
                    "Authorization": self.api_key,
                    "User-Agent": self.version
                },
                **kwargs
            )
            return response

    async def create_url(
        self,
        url: str,
        description: str = "Python Plume URL API Wrapper",
        expire_at: int = 0,
        custom_id: str = "",
    ):
        if len(custom_id) > 500:
            raise Exception("Custom ID cannot be longer than '500' characters")
        res = await self.request(
            "POST",
            "/create",
            json={
                "url": url,
                "description": description,
                "expiresAt": expire_at,
                "customId": custom_id,
            },
        )
        print(res.status)
        if res.status != 200:

            raise Exception((await res.json())["message"])

        return (await res.json())["shorten"]

    async def search_url(
        self, custom_id: str, limit: int = 10, page: int = 1, expire_at: int = 0
    ):
        if len(custom_id) > 500:
            raise Exception("Custom ID cannot be longer than '500' characters")
        res = await self.request(
            "GET",
            "/search",
            params={
                "customId": custom_id,
                "limit": limit,
                "page": page,
                "expiresAt": expire_at,
            },
        )
        if res.status != 200:
            raise Exception(res.json()["message"])
        return await res.json()

    async def get_url(self, id: str = ""):
        if len(id) < 8:
            raise Exception("ID cannot be shorter than '8' characters")
        if len(id) > 16:
            raise Exception("ID cannot be longer than '16' characters")

        res = await self.request("GET", "/urls/{0}".format(id), params={"id": id})
        if res.status != 200:
            raise Exception((await res.json())["message"])
        return await res.json()

    async def edit_url(
        self,
        id: str,
        url: str,
        expire_at: int = None,
        description: str = None,
        custom_id: str = "",
    ):
        if len(id) < 8:
            raise Exception("ID cannot be shorter than '8' characters")
        if len(id) > 16:
            raise Exception("ID cannot be longer than '16' characters")
        if len(custom_id) > 500:
            raise Exception("Custom ID cannot be longer than '500' characters")

        res = await self.request(
            "PATCH",
            "/urls/{0}".format(id),
            json={
                "url": url,
                "expiresAt": expire_at,
                "description": description,
                "customId": custom_id,
            },
        )
        if res.status != 200:
            raise Exception(res.json()["message"])
        return res.json()

    async def delete_url(self, id: str):
        if len(id) < 8:
            raise Exception("ID cannot be shorter than '8' characters")
        if len(id) > 16:
            raise Exception("ID cannot be longer than '16' characters")

        res = await self.request("DELETE", "/urls/{0}".format(id))
        if res.status != 200:
            raise Exception(res.json()["message"])
        return await res.json()
