# built in
import re

# mine
from .llm_apis.kobold import KoboldClient
from . import template


class Prompter:
    stop_pattern = re.compile(r"```|###|</")
    autoextend = True

    def __init__(self):
        self.llm_client = KoboldClient("http://localhost:5001/api")

    async def connect(self):
        await self.llm_client.connect()

    async def prompt(
        self, system_prompt: str, prompt: str, prefix: str = "", history=[]
    ):
        response = ""
        while True:
            prompt = template.LIMARP3_SHORT(
                system_prompt, history, prompt, prefix, response
            )
            new = await self.llm_client.generate(prompt)

            if not new:
                return response

            response += new
            m = self.stop_pattern.search(response)
            if m is not None:
                response = response[: m.start(0)]
                return response

            if not self.autoextend:
                return response
