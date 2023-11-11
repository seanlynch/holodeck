# built-in
import asyncio
import json
from typing import Any

# third party
import aiohttp


class KoboldClient:
    def __init__(self, endpoint: str, settings: dict[str, Any]):
        self.endpoint = endpoint.rstrip("/")
        self.version = None
        self.max_context_length = None
        self.max_length = None
        self.settings = settings

    def url(self, path: str) -> str:
        return f"{self.endpoint}{path}"

    async def get(self, path: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url(path)) as resp:
                return await resp.json()

    async def post(self, path: str, data: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url(path), data=json.dumps(data)) as resp:
                return await resp.json()

    async def get_max_context_length(self) -> int:
        return (await self.get("/v1/config/max_context_length"))["value"]

    async def get_max_length(self) -> int:
        return (await self.get("/v1/config/max_length"))["value"]

    async def get_version(self) -> str:
        return (await self.get("/v1/info/version"))["result"]

    async def tokencount(self, prompt: str) -> int:
        data = {"prompt": prompt}
        return (await self.post("/extra/tokencount", data))["value"]

    async def generate(self, prompt: str):
        data = {
            **self.settings,
            "prompt": prompt,
        }

        resp = await self.post("/v1/generate", data)
        results = resp["results"]
        assert len(results) == 1
        return results[0]["text"]

    async def connect(self):
        self.version = await self.get_version()
        self.max_context_length = await self.get_max_context_length()
        self.max_length = await self.get_max_length()
